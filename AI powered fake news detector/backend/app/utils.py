from PIL import Image, UnidentifiedImageError
import requests
from io import BytesIO
import torchvision.transforms as transforms
import torch

def preprocess_image_from_url(image_url: str) -> torch.Tensor:
    try:
        print(f"Fetching image from URL: {image_url}")
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(image_url, headers=headers, timeout=10)
        response.raise_for_status()

        content_type = response.headers.get('Content-Type', '')
        print(f"Content-Type: {content_type}")
        
        if 'image' not in content_type:
            print(f"Error: Content-Type is not an image: {content_type}")
            return None

        print("Opening image...")
        image = Image.open(BytesIO(response.content)).convert("RGB")
        print(f"Image opened successfully. Size: {image.size}")
        
        transform = transforms.Compose([
            transforms.Resize((224, 224)),
            transforms.ToTensor(),
            transforms.Normalize(mean=[0.485, 0.456, 0.406],
                                 std=[0.229, 0.224, 0.225]),
        ])
        
        print("Applying transformations...")
        tensor = transform(image).unsqueeze(0)
        print(f"Image transformed to tensor of shape: {tensor.shape}")
        return tensor

    except requests.RequestException as e:
        print(f"Request error: {str(e)}")
        return None
    except UnidentifiedImageError as e:
        print(f"Image identification error: {str(e)}")
        return None
    except Exception as e:
        print(f"Unexpected error in image processing: {str(e)}")
        import traceback
        traceback.print_exc()
        return None
