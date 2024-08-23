from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

# Load the model when the Flask app starts
with open('modelo_gradient_boosting.pkl', 'rb') as f:
    model = pickle.load(f)

@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        data = request.json
        print("Received data:", data)  # Debugging: Print the received JSON data

        try:
            AirTemperature = float(data["Air temperature [K]"])
            ProcessTemperature = float(data["Process temperature [K]"])
            RotationalSpeed = int(data["Rotational speed [rpm]"])
            Torque = float(data["Torque [Nm]"])
            ToolWear = int(data["Tool wear [min]"])
            Type__H = int(data["Type__H"])
            Type__L = int(data["Type__L"])
            Type__M = int(data["Type__M"])

            model_input = np.array([[AirTemperature, ProcessTemperature, RotationalSpeed, Torque, ToolWear, Type__H, Type__L, Type__M]])
            print("Model input:", model_input)  # Debugging: Print the model input

            prediction = model.predict(model_input)
            print("Prediction:", prediction)  # Debugging: Print the prediction result

            # Return the result based on the prediction
            if prediction[0] == 1:
                return jsonify({"result": "defect"})
            else:
                return jsonify({"result": "working"})

        except Exception as e:
            print("Error:", str(e))  # Debugging: Print any errors encountered
            return jsonify({"error": str(e)}), 500

    else:
        return jsonify({"error": "Invalid request method"}), 405

if __name__ == "__main__":
    app.run(debug=True)
