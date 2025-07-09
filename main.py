from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

app = FastAPI()

# Load model and tokenizer
model_path = "model"  # your saved model directory
tokenizer = AutoTokenizer.from_pretrained(model_path)
model = AutoModelForSequenceClassification.from_pretrained(model_path)
sentiment_pipeline = pipeline(
    "sentiment-analysis", model=model, tokenizer=tokenizer)

# Request format


class FeedbackRequest(BaseModel):
    text: str


@app.post("/predict")
def predict_sentiment(data: FeedbackRequest):
    result = sentiment_pipeline(data.text)[0]
    label = result["label"].lower()
    confidence = round(result["score"], 2)
    return {"sentiment": label, "confidence": confidence}
