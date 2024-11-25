import unittest
from flask import Flask
from bson import ObjectId
from app import decks_bp, questions_bp, users_bp

# Create a test Flask app
app = Flask(__name__)
app.register_blueprint(decks_bp, url_prefix='/api')
app.register_blueprint(questions_bp, url_prefix='/api')
app.register_blueprint(users_bp, url_prefix='/api')
app.testing = True


class TestUsersAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        print("Test finished")

    def test_create_user(self):
        # Arrange
        user_data = {
            "name": "Math Quiz",
            "time_to_complete": 60,
            "questions": []
        }

        # Act
        response = self.client.post('/api/users', json=user_data)

        # Assert
        self.assertEqual(201, response.status_code)
        self.assertIn("_id", response.json)

        # Cleanup
        self.client.delete(f'/api/users/{response.json["_id"]}')

    def test_get_users(self):
        # Arrange
        mock_users = [
            {"decks": [], "email": "test1@example.com", "name": "Test User 1", "password": "testPass123"},
            {"decks": [], "email": "test2@example.com", "name": "Test User 2", "password": "testPass123"}
        ]

        # Act
        response = self.client.get('/api/users')

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response.json, list)

    def test_get_user(self):
        # Arrange
        mock_user = {"decks": [], "email": "test1@example.com", "name": "Test User 1", "password": "testPass123"}
        response = self.client.post('/api/users', json=mock_user)
        user_id = response.get_json()["_id"]

        # Act
        response = self.client.get(f'/api/users/{user_id}')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["_id"], str(user_id))
        self.assertEqual(len(response.json["decks"]), 0)

        # Cleanup
        self.client.delete(f'/api/users/{user_id}')

    def test_update_user(self):
        # Arrange
        mock_user = {"decks": [], "email": "test1@example.com", "name": "Test User 1", "password": "testPass123"}
        response = self.client.post('/api/users', json=mock_user)
        user_id = response.get_json()["_id"]
        updated_data = {"name": "Clark Kent"}

        # Act
        response = self.client.put(f'/api/users/{user_id}', json=updated_data)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json["matched_count"], 1)

        # Cleanup
        self.client.delete(f'/api/users/{user_id}')

    def test_delete_user(self):
        # Arrange
        mock_user = {"decks": [], "email": "test1@example.com", "name": "Test User 1", "password": "testPass123"}
        response = self.client.post('/api/users', json=mock_user)
        print(response)
        user_id = response.get_json()["_id"]

        # Act
        response = self.client.delete(f'/api/users/{user_id}')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["deleted_count"], 1)


if __name__ == '__main__':
    unittest.main()
