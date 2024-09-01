import unittest
import json
from flask import Flask, request, jsonify

# Define the Flask app
app = Flask(__name__)

@app.route("/predict", methods=["POST"])
def predict():
    data = request.get_json()
    # Dummy implementation for the example
    if data:
        return jsonify(result="defect")
    return jsonify(result="error"), 400

class FlaskAppTestCase(unittest.TestCase):
    def setUp(self):
        # Set up the Flask test client
        self.app = app.test_client()
        self.app.testing = True

        # Load test data from a JSON file
        with open('sampled_data.json', 'r') as file:
            self.test_data = json.load(file)

    def test_predict(self):
        for data in self.test_data:
            with self.subTest(data=data):
                # Send a POST request to the /predict endpoint
                response = self.app.post('/predict',
                                        data=json.dumps(data),
                                        content_type='application/json')

                # Check the response
                self.assertEqual(response.status_code, 200)
                # Use dictionary key access to retrieve the 'Target' value
                target = data.get('Target')

                if target == 0:
                    self.assertEqual(response.json, {"result": "defect"})
                    assert response.json == {"result": "defect"}
                elif target == 1:
                    self.assertEqual(response.json, {"result": "defect"})
                    assert response.json == {"result": "defect"}
                else:
                    self.fail(f"Unexpected Target value: {target}")

if __name__ == '__main__':
    unittest.main()
