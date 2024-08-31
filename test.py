import unittest
import json
from flask import Flask, request, jsonify

# Assuming your Flask app is defined here or imported from another module
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
        
    

    def test_predict(self):
        # Define the payload
        payload = {
        "Air temperature [K]": 303.3,
        "Process temperature [K]": 311.6,
        "Rotational speed [rpm]": 1337,
        "Torque [Nm]": 56.8,
        "Tool wear [min]": 187,
        "Type__H": 0,
        "Type__L": 1,
        "Type__M": 0
    }

        # Send a POST request to the /predict endpoint
        response = self.app.post('/predict',
                                data=json.dumps(payload),
                                content_type='application/json')

        # Check the response
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json, {"result": "defect"})


if __name__ == '__main__':
    unittest.main()
