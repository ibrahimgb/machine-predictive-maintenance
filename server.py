from flask import Flask, render_template, request
import pickle
import pandas as pd


app = Flask(__name__)
model = pickle.load(open("modelo_gradient_boosting.pkl", "rb"))


def model_pred(features):
    test_data = pd.DataFrame([features])
    prediction = model.predict(test_data)
    return int(prediction[0])

@app.route("/predict", methods=["POST"])
def predict():
    if request.method == "POST":
        data = request.json

        # Extracting data from the JSON object
        AirTemperature = float(data["Air temperature [K]"])
        ProcessTemperature = float(data["Process temperature [K]"])
        RotationalSpeed = int(data["Rotational speed [rpm]"])
        Torque = float(data["Torque [Nm]"])
        ToolWear = int(data["Tool wear [min]"])
        Type__H = int(data["Type__H"])
        Type__L = int(data["Type__L"])
        Type__M = int(data["Type__M"])

        # Create a numpy array for the model input
        model_input = np.array([[AirTemperature, ProcessTemperature, RotationalSpeed, Torque, ToolWear, Type__H, Type__L, Type__M]])

        # Make a prediction using the loaded model
        prediction = model.predict(model_input)

        # Return the result based on the prediction
        if prediction[0] == 1:
            return jsonify({"result": "defect"})
        else:
            return jsonify({"result": "working"})

    else:
        return jsonify({"error": "Invalid request method"}), 405

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
