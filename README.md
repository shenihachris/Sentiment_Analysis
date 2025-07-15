# Sentiment_Analysis

Sentiment analysis for structured and unstructured feedback

Download model : https://www.kaggle.com/code/shenihachris/sentimment-analysis-kaggle

1. Start FastAPI (Terminal 1)
file name: main.py
new terminal : uvicorn main:app --reload

Test at: http://127.0.0.1:8000/docs

3. Start Flask WhatsApp Bot (Terminal 2)
file name: whatsapp_bot.py
new terminal: python whatsapp_bot.py

3. Start ngrok (Terminal 3)
   type > ngrok http 8000
Copy the HTTPS forwarding URL (e.g., https://abcd1234.ngrok-free.app)

5. Set Twilio Sandbox Webhook
Twilio --> Messaging --> Try it out --> Send a whatsapp message
-----> Sandbox setting --> "When message comes in" , paste
   
https://abcd1234.ngrok-free.app/whatsapp(from ngrok)
Click Save 


 
 WhatsApp Flow Test

 join usual-fastened
Send this to Twilio sandbox WhatsApp number:

Hi
Then reply with:
3
Then:
feedback message


