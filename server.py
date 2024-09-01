from flask import Flask, request, jsonify
import pickle
import numpy as np

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv
import os
from email.message import EmailMessage
import ssl
import smtplib
import json

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

@app.route("/contact", methods=["POST"])
def sendAlertToContacts():
    # Load the JSON data from the file
    load_dotenv()
    
    file_path = os.getenv("CONTACTS") #'data/contact.json'
    print(file_path)
    with open(file_path, 'r') as file:
        data = json.load(file)
    
    # List to collect all emails
    emails = []

    # Iterate over each section in the JSON data
    for section in data:
        for person in data[section]:
            # Append the email to the list if it exists
            email = person.get("email")
            if email:
                emails.append(email)
    
    # Print all collected emails
    for email in emails:
        send_email(email)



def send_email(to_email):
    # Load environment variables from .env file
    load_dotenv()

    # Email account credentials from environment variables
    from_email = os.getenv("EMAIL_ADDRESS")
    from_password = os.getenv("EMAIL_PASS")
    #to_email="ibrahim.guoual.b@gmail.com"
    print(from_password)
    # Email content
    subject = "Potontial machine Failier"
    body= "Alerting for a potential machin falier in "

    # Create the email
    msg = EmailMessage()
    msg['From'] = from_email
    msg['To'] = to_email
    msg['Subject'] = subject
    msg.set_content(body)

    context = ssl.create_default_context()
    
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as smtp:
        smtp.login(from_email, from_password)
        smtp.sendmail(from_email, to_email, msg.as_string())

if __name__ == "__main__":
    app.run(debug=True)
