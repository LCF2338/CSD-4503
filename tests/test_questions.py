import unittest
from flask import Flask
from bson import ObjectId
from app import questions_bp


# Create a test Flask app
app = Flask(__name__)
app.register_blueprint(questions_bp, url_prefix='/api')
app.testing = True


class TestQuestionsAPI(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def tearDown(self):
        print("Test finished")

    def test_create_question(self):
        # Arrange
        question_data = {
            "question_text": "What is the capital of France?",
            "question_answer": "Paris",
            "question_img": None,
            "difficulty": 1
        }

        # Act
        response = self.client.post('/api/questions', json=question_data)

        # Assert
        self.assertEqual(201, response.status_code)
        self.assertIn("_id", response.json)

        # Cleanup
        self.client.delete(f'/api/questions/{response.json["_id"]}')

    def test_get_questions(self):
        # Arrange
        question_data = [
            {"_id": ObjectId(), "question_text": "Test question", "question_answer": "Answer"}
        ]
        # Act
        response = self.client.get('/api/questions')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertIsInstance(response.json, list)

    def test_get_question(self):
        # Arrange
        response = self.client.post('/api/questions', json={
            "question_text": "What is the capital of France?",
            "question_answer": "Paris",
            "question_img": "image_url",
            "difficulty": 1
        })
        question_id = response.get_json()["_id"]

        # Act
        response = self.client.get(f'/api/questions/{question_id}')

        # Assert
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["question_text"], "What is the capital of France?")

        # Cleanup
        self.client.delete(f'/api/questions/{response.json["_id"]}')

    def test_update_question(self):
        # Arrange
        response = self.client.post('/api/questions', json={
            "question_text": "What is the capital of Belgium?",
            "question_answer": "Brussels",
            "question_img": "image_url",
            "difficulty": 2
        })
        question_id = response.get_json()["_id"]
        update_data = {"question_text": "Updated question"}

        # Act
        response = self.client.put(f'/api/questions/{question_id}', json=update_data)

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["matched_count"], 1)

        # Cleanup
        self.client.delete(f'/api/questions/{question_id}')

    def test_delete_question(self):
        # Arrange
        response = self.client.post('/api/questions', json={
            "question_text": "What is the capital of Belgium?",
            "question_answer": "Brussels",
            "question_img": "image_url",
            "difficulty": 2
        })
        question_id = response.get_json()["_id"]

        # Act
        response = self.client.delete(f'/api/questions/{question_id}')

        # Assert
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json["deleted_count"], 1)


if __name__ == '__main__':
    unittest.main()
