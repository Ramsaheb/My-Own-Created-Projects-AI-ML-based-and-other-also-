from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Optional
from app.utils import preprocess_image_from_url  # renamed for clarity
from app.model import MultiModalModel
import torch
from transformers import BertTokenizer

app = FastAPI()

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = MultiModalModel(num_labels=6).to(device)
model.load_state_dict(torch.load("app/models/multimodal_model.pth", map_location=device))
model.eval()

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

class_names = ["real", "fake", "satire", "clickbait", "bias", "conspiracy"]

class InputData(BaseModel):
    text: str
    image_url: Optional[str] = None  # Make sure this matches your frontend key

@app.post("/predict")
async def predict(data: InputData):
    try:
        inputs = tokenizer(data.text, padding='max_length', truncation=True, max_length=128, return_tensors="pt")
        input_ids = inputs["input_ids"].to(device)
        attention_mask = inputs["attention_mask"].to(device)

        if data.image_url is None:
            raise HTTPException(status_code=400, detail="image_url is required.")

        image_tensor = preprocess_image_from_url(data.image_url)
        if image_tensor is None:
            raise HTTPException(status_code=400, detail="Image could not be processed. Please check the URL or file format.")

        image_tensor = image_tensor.to(device)

        with torch.no_grad():
            outputs = model(input_ids=input_ids, attention_mask=attention_mask, image=image_tensor)
            predicted_class = torch.argmax(outputs, dim=1).item()
            label = class_names[predicted_class]

        return {
            "label": label,
            "confidence": float(torch.softmax(outputs, dim=1)[0][predicted_class])
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
