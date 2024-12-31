# from fastapi import FastAPI, File, UploadFile, HTTPException
# from fastapi.responses import HTMLResponse
# from PIL import Image
# import numpy as np
# import tensorflow as tf
# import io

# app = FastAPI()

# # Load the trained TensorFlow model
# model = tf.keras.models.load_model(r"C:\Users\Ramsaheb Prasad\Desktop\Ai image detector\final_model.h5")

# def verify_image(image: np.ndarray) -> str:
#     # Resize image to match model input size
#     image = tf.image.resize(image, (128, 128))  # Resize to (128, 128)
#     # Normalize pixel values
#     image = image / 255.0
#     # Make prediction using the loaded model
#     prediction = model.predict(tf.expand_dims(image, axis=0))[0]
#     # Convert prediction to human-readable format
#     return "AI-generated" if prediction >= 0.5 else "Real"

# @app.post("/upload/")
# async def upload_image(file: UploadFile = File(...)):
#     # Check if the uploaded file is an image
#     if not file.content_type.startswith("image"):
#         raise HTTPException(status_code=400, detail="Uploaded file is not an image")

#     # Read the uploaded image file
#     content = await file.read()
#     image = np.array(Image.open(io.BytesIO(content)))

#     # Perform image verification
#     verification_result = verify_image(image)

#     return {"verification_result": verification_result}

# @app.get("/", response_class=HTMLResponse)
# async def home():
#     html_content = """
#     <!DOCTYPE html>
#     <html lang="en">
#     <head>
#         <meta charset="UTF-8">
#         <meta name="viewport" content="width=device-width, initial-scale=1.0">
#         <title>Image Classifier</title>
#         <style>
#             body {
#                 font-family: Arial, sans-serif;
#                 display: flex;
#                 justify-content: center;
#                 align-items: center;
#                 height: 100vh;
#                 margin: 0;
#                 background-color: #f0f0f0;
#             }
#             .container {
#                 text-align: center;
#                 background: #fff;
#                 padding: 20px;
#                 border-radius: 8px;
#                 box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
#             }
#             input[type="file"] {
#                 margin: 10px 0;
#             }
#             button {
#                 padding: 10px 20px;
#                 font-size: 16px;
#                 cursor: pointer;
#             }
#             .result {
#                 margin-top: 20px;
#                 font-size: 18px;
#                 font-weight: bold;
#             }
#         </style>
#     </head>
#     <body>
#         <div class="container">
#             <h1>Image Classifier</h1>
#             <input type="file" id="fileInput" />
#             <button onclick="uploadImage()">Upload Image</button>
#             <div id="result" class="result"></div>
#         </div>

#         <script>
#             async function uploadImage() {
#                 const fileInput = document.getElementById('fileInput');
#                 const resultDiv = document.getElementById('result');
#                 const file = fileInput.files[0];
                
#                 if (!file) {
#                     resultDiv.textContent = 'Please select an image file first.';
#                     return;
#                 }

#                 const formData = new FormData();
#                 formData.append('file', file);

#                 try {
#                     const response = await fetch('/upload/', {
#                         method: 'POST',
#                         body: formData
#                     });

#                     if (!response.ok) {
#                         throw new Error('Network response was not ok.');
#                     }

#                     const data = await response.json();
#                     resultDiv.textContent = `Verification Result: ${data.verification_result}`;
#                 } catch (error) {
#                     resultDiv.textContent = `Error: ${error.message}`;
#                 }
#             }
#         </script>
#     </body>
#     </html>
#     """
#     return HTMLResponse(content=html_content)



from fastapi import FastAPI, File, UploadFile, HTTPException
from fastapi.responses import HTMLResponse
from PIL import Image
import numpy as np
import tensorflow as tf
import io
import os

app = FastAPI()

# Define the relative path to the model
model_path = os.path.join(os.path.dirname(__file__), "final_model.h5")

# Check if the model file exists
if not os.path.exists(model_path):
    raise FileNotFoundError(f"Model file not found at {model_path}")

# Load the trained TensorFlow model
model = tf.keras.models.load_model(model_path)

def verify_image(image: np.ndarray) -> str:
    # Ensure image is in the expected shape (128, 128, 3)
    if image.shape[-1] != 3:
        raise ValueError("Image must have 3 color channels (RGB)")

    # Resize image to match model input size
    image = tf.image.resize(image, (128, 128))  # Resize to (128, 128)
    # Normalize pixel values
    image = image / 255.0
    # Make prediction using the loaded model
    prediction = model.predict(tf.expand_dims(image, axis=0))[0]
    # Convert prediction to human-readable format
    return "AI-generated" if prediction >= 0.5 else "Real"

@app.post("/upload/")
async def upload_image(file: UploadFile = File(...)):
    # Check if the uploaded file is an image
    if not file.content_type.startswith("image"):
        raise HTTPException(status_code=400, detail="Uploaded file is not an image")

    try:
        # Read the uploaded image file
        content = await file.read()
        image = Image.open(io.BytesIO(content))

        # Convert image to RGB if it has an alpha channel
        if image.mode in ("RGBA", "P"):
            image = image.convert("RGB")

        image = np.array(image)

        # Perform image verification
        verification_result = verify_image(image)

        return {"verification_result": verification_result}
    except Exception as e:
        # Return detailed error message for debugging
        return {"error": str(e)}

@app.get("/", response_class=HTMLResponse)
async def home():
    html_content = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Image Classifier</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background-color: #f0f0f0;
        }
        .container {
            text-align: center;
            background: #fff;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 0 10px rgba(0, 0, 0, 0.1);
        }
        input[type="file"] {
            margin: 10px 0;
        }
        button {
            padding: 10px 20px;
            font-size: 16px;
            cursor: pointer;
        }
        .result {
            margin-top: 20px;
            font-size: 18px;
            font-weight: bold;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Image Classifier</h1>
        <input type="file" id="fileInput" />
        <button onclick="uploadImage()">Upload Image</button>
        <div id="result" class="result"></div>
    </div>

    <script>
        async function uploadImage() {
            const fileInput = document.getElementById('fileInput');
            const resultDiv = document.getElementById('result');
            const file = fileInput.files[0];
            
            if (!file) {
                resultDiv.textContent = 'Please select an image file first.';
                return;
            }

            const formData = new FormData();
            formData.append('file', file);

            try {
                const response = await fetch('/upload/', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error('Network response was not ok.');
                }

                const data = await response.json();
                if (data.error) {
                    resultDiv.textContent = `Error: ${data.error}`;
                } else {
                    resultDiv.textContent = `Verification Result: ${data.verification_result}`;
                }
            } catch (error) {
                resultDiv.textContent = `Error: ${error.message}`;
            }
        }
    </script>
</body>
</html>
    """
    return HTMLResponse(content=html_content)
