# Save as server.py
from flask import Flask, request, jsonify
import joblib
import pickle


app = Flask(__name__)
# Load model
model = pickle.load(open("modelo_gradient_boosting.pkl", "rb"))

@app.route('/post_data', methods=['POST'])
def post_data():
    data = request.get_json()
    if data:
        return jsonify({"status": "success", "received_data": data}), 200
    else:
        return jsonify({"status": "error", "message": "Invalid JSON"}), 400


@app.route('/predict', methods=['POST'])
def predict():
    # Get the JSON data from the request
    data = request.get_json()

    # Assuming the data is sent as a list of features for prediction
    features = np.array(data['features']).reshape(1, -1)

    # Make a prediction
    prediction = model.predict(features)

    # Return the prediction result as JSON
    return jsonify({'prediction': prediction.tolist()})

if __name__ == '__main__':
    app.run(debug=True, port=5000)