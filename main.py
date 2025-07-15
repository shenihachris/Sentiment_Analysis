from fastapi import FastAPI
from pydantic import BaseModel
from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline

app = FastAPI()

# ✅ Load model from local folder
model_path = "./model"

tokenizer = AutoTokenizer.from_pretrained(model_path, local_files_only=True)
model = AutoModelForSequenceClassification.from_pretrained(
    model_path, local_files_only=True)

sentiment_pipeline = pipeline(
    "sentiment-analysis", model=model, tokenizer=tokenizer)


class FeedbackRequest(BaseModel):
    text: str


@app.post("/predict")
def predict_sentiment(data: FeedbackRequest):
    result = sentiment_pipeline(data.text)[0]
    return {
        "sentiment": result["label"].lower(),
        "confidence": round(result["score"], 2)
    }
