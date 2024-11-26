import unittest
from flask import Flask
from bson import ObjectId
from app import decks_bp, questions_bp

# Create a test Flask app
app = Flask(__name__)
app.register_blueprint(decks_bp, url_prefix='/api')
app.register_blueprint(questions_bp, url_prefix='/api')
app.testing = True


class TestDecksAPI(unittest.TestCase):

    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        print("Test finished")

    def test_create_deck(self):
        # Arrange
        deck_data = {
            "name": "Math Quiz",
            "time_to_complete": 60,
            "questions": []
        }

        # Act
        response = self.client.post('/api/decks', json=deck_data)

        # Assert
        self.assertEqual(201, response.status_code)
        self.assertIn("_id", response.json)

        # Cleanup
        self.client.delete(f'/api/decks/{response.json["_id"]}')

    def test_get_decks(self):
        # Arrange
        mock_decks = [
            {"_id": ObjectId(), "name": "Math Quiz", "time_to_complete": 60, "questions": []},
            {"_id": ObjectId(), "name": "Science Quiz", "time_to_complete": 120, "questions": []}
        ]

        # Act
        response = self.client.get('/api/decks')

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertIsInstance(response.json, list)

    def test_get_deck(self):
        # Arrange
        response = self.client.post('/api/questions', json={
            "question_text": "What is 3+3?",
            "question_answer": "6",
            "question_img": "image_url",
            "difficulty": 1
        })
        question_id = response.get_json()["_id"]

        mock_deck = {
            "name": "Math Quiz",
            "time_to_complete": 60,
            "questions": [question_id]
        }
        response = self.client.post('/api/decks', json=mock_deck)
        deck_id = response.get_json()["_id"]

        # Act
        response = self.client.get(f'/api/decks/{deck_id}')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["_id"], str(deck_id))
        self.assertEqual(len(response.json["questions"]), 1)

        # Cleanup
        self.client.delete(f'/api/decks/{deck_id}')
        self.client.delete(f'/api/questions/{question_id}')

    def test_update_deck(self):
        # Arrange
        mock_deck = {
            "name": "Math Quiz",
            "time_to_complete": 60,
            "questions": []
        }
        response = self.client.post('/api/decks', json=mock_deck)
        deck_id = response.get_json()["_id"]
        updated_data = {"name": "Updated Quiz"}

        # Act
        response = self.client.put(f'/api/decks/{deck_id}', json=updated_data)

        # Assert
        self.assertEqual(200, response.status_code)
        self.assertEqual(response.json["matched_count"], 1)

        # Cleanup
        self.client.delete(f'/api/decks/{deck_id}')

    def test_delete_deck(self):
        # Arrange
        mock_deck = {
            "name": "Math Quiz",
            "time_to_complete": 60,
            "questions": []
        }
        response = self.client.post('/api/decks', json=mock_deck)
        deck_id = response.get_json()["_id"]

        # Act
        response = self.client.delete(f'/api/decks/{deck_id}')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.get_json()["deleted_count"], 1)


if __name__ == '__main__':
    unittest.main()
