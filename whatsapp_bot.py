from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from pymongo import MongoClient
import requests
import re
import datetime

app = Flask(__name__)

# Connect to local MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["feedback_db"]
collection = db["whatsapp_feedback"]

# Your FastAPI sentiment analysis endpoint
SENTIMENT_API = "http://127.0.0.1:8000/predict"


@app.route("/whatsapp", methods=["POST"])
def whatsapp_feedback():
    incoming_msg = request.values.get("Body", "").strip()
    user_number = request.values.get("From", "")
    timestamp = datetime.datetime.utcnow()

    response = MessagingResponse()
    msg = response.message()

    match = re.match(
        r"Rating[:\- ]?(\d)[\s\n]+Feedback[:\- ]?(.*)", incoming_msg, re.IGNORECASE)

    if match:
        rating = int(match.group(1))
        feedback = match.group(2)

        # Call the sentiment model
        result = requests.post(SENTIMENT_API, json={"text": feedback}).json()
        sentiment = result.get("sentiment", "unknown").lower()
        confidence = result.get("confidence", 0.0)

        # Save to MongoDB
        collection.insert_one({
            "user": user_number,
            "timestamp": timestamp,
            "rating": rating,
            "feedback": feedback,
            "sentiment": sentiment,
            "confidence": confidence
        })

        # Respond to user
        if rating <= 3 and sentiment == "negative":
            msg.body(
                "We're sorry to hear that. 😔\nYou can escalate this to: support@yourcompany.com")
        else:
            msg.body("Thanks for your feedback! ✅")
    else:
        msg.body(
            "Please send in this format:\nRating: 4\nFeedback: The ride was good.")

    return str(response)


if __name__ == "__main__":
    app.run(debug=True)
