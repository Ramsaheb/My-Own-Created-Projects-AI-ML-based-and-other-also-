from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
import torchvision.transforms as transforms
import torch

def preprocess_image_from_url(image_url: str) -> torch.Tensor | None:
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(image_url, headers=headers, timeout=10)
        response.raise_for_status()

        if 'image' not in response.headers.get('Content-Type', ''):
            return None

        image = Image.open(BytesIO(response.content)).convert("RGB")
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),
        ])
        return transform(image).unsqueeze(0)

    except (requests.RequestException, UnidentifiedImageError, Exception):
        return None
