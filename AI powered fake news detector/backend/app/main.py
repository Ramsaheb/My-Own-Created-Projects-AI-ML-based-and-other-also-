from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from app.utils import preprocess_image_from_url  # renamed for clarity
from app.model import MultiModalModel
import torch
from transformers import BertTokenizer
import os

app = FastAPI()

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
model = MultiModalModel(num_labels=6).to(device)

# Get model path from environment variable or use default path
model_path = os.environ.get('MODEL_PATH')

# If environment variable is not set, try to find the model
if not model_path:
    # Try local development path
    model_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "app", "models", "multimodal_model.pth")
    
    # If not found, try a simpler relative path for local development
    if not os.path.exists(model_path):
        model_path = "./app/models/multimodal_model.pth"
        
    # If still not found, use Docker path
    if not os.path.exists(model_path):
        model_path = "/app/app/models/multimodal_model.pth"

print(f"Loading model from: {model_path}")
try:
    # Check if model file exists
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at {model_path}")
        
    # Load model with error handling
    state_dict = torch.load(model_path, map_location=device)
    print(f"Model loaded successfully. Keys: {list(state_dict.keys())[:5]}...")
    
    model.load_state_dict(state_dict)
    print("Model state dictionary loaded successfully")
    model.eval()
    print("Model set to evaluation mode")
except Exception as e:
    print(f"Error loading model: {str(e)}")
    import traceback
    traceback.print_exc()
    raise RuntimeError(f"Failed to load model: {str(e)}")

tokenizer = BertTokenizer.from_pretrained("bert-base-uncased")

class_names = ["real", "fake", "satire", "clickbait", "bias", "conspiracy"]

class InputData(BaseModel):
    text: str
    image_url: Optional[str] = None  # Make sure this matches your frontend key

@app.post("/predict")
async def predict(data: InputData):
    try:
        print(f"Received prediction request with text: {data.text[:50]}... and image URL: {data.image_url}")
        
        inputs = tokenizer(data.text, padding='max_length', truncation=True, max_length=128, return_tensors="pt")
        input_ids = inputs["input_ids"].to(device)
        attention_mask = inputs["attention_mask"].to(device)

        image_tensor = None
        if data.image_url and data.image_url.strip() != "":
            print("Processing image from URL...")
            image_tensor = preprocess_image_from_url(data.image_url)
            if image_tensor is None:
                print("Warning: Image could not be processed. Falling back to text-only mode.")
            else:
                print("Image processed successfully, moving to device...")
                image_tensor = image_tensor.to(device)
        else:
            print("No image URL provided. Using text-only mode.")

        print("Running model prediction...")
        with torch.no_grad():
            outputs = model(input_ids=input_ids, attention_mask=attention_mask, image=image_tensor)
            predicted_class = torch.argmax(outputs, dim=1).item()
            label = class_names[predicted_class]
            confidence = float(torch.softmax(outputs, dim=1)[0][predicted_class])
            
            # Add a note if text-only mode was used
            mode = "text-only" if image_tensor is None else "multimodal"
        
        print(f"Prediction complete: {label} with confidence {confidence}, mode: {mode}")
        return {
            "label": label,
            "confidence": confidence,
            "mode": mode
        }
    except Exception as e:
        print(f"Error in prediction: {str(e)}")
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)