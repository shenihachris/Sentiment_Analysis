from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import datetime

app = Flask(__name__)

# FastAPI endpoint
SENTIMENT_API = "http://127.0.0.1:8000/predict"

# In-memory session state
user_state = {}


@app.route("/whatsapp", methods=["POST"])
def whatsapp_feedback():
    incoming_msg = request.values.get("Body", "").strip()
    user = request.values.get("From", "")
    timestamp = datetime.datetime.utcnow()

    print(f"[{timestamp}] From {user}: {incoming_msg}")

    response = MessagingResponse()
    msg = response.message()

    # Step 1: New user starts chat
    if user not in user_state:
        user_state[user] = {"step": "awaiting_rating"}
        msg.body("Hi! 👋 What is your rating for the ride? (1 to 5)")
        return str(response)

    # Step 2: Collect rating
    elif user_state[user]["step"] == "awaiting_rating":
        if incoming_msg.isdigit() and 1 <= int(incoming_msg) <= 5:
            user_state[user]["rating"] = int(incoming_msg)
            user_state[user]["step"] = "awaiting_feedback"
            msg.body("Thanks! 🙏 Now please share your feedback about the ride.")
        else:
            msg.body("⚠️ Please reply with a number between 1 and 5.")
        return str(response)

    # Step 3: Collect feedback
    elif user_state[user]["step"] == "awaiting_feedback":
        feedback = incoming_msg
        rating = user_state[user]["rating"]

        try:
            result = requests.post(SENTIMENT_API, json={
                                   "text": feedback}).json()
            sentiment = result.get("sentiment", "unknown").lower()
            confidence = result.get("confidence", 0.0)
        except Exception as e:
            print("[ERROR] Sentiment API failed:", e)
            sentiment = "unknown"
            confidence = 0.0

        print(
            f"[SENTIMENT] Rating: {rating}, Feedback: {feedback}, Sentiment: {sentiment}, Confidence: {confidence}")

        if rating <= 2 and sentiment == "negative":

            msg.body(
                "😔 We're sorry to hear that.\nPlease raise a complaint at: shenihachris@gmail.com")
        else:
            msg.body(
                "✅ Thank you for your feedback! Have a great day!")

        # End session
        del user_state[user]
        return str(response)

    # Fallback
    msg.body("Something went wrong. Please say 'Hi' to start again.")
    return str(response)


if __name__ == "__main__":
    app.run(debug=True)
