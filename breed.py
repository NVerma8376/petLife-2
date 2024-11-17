import tensorflow as tf
from tensorflow.keras.applications import ResNet50V2
from tensorflow.keras.preprocessing import image
from tensorflow.keras.applications.resnet_v2 import preprocess_input, decode_predictions
import numpy as np
import cv2
import base64
from io import BytesIO
from PIL import Image
from data import image_base64  # Import base64 image data

# Load ResNet50V2 pre-trained model
model = ResNet50V2(weights='imagenet')

# Function to predict dog breed from base64 image data
def predict_breed_from_base64(image_base64_data):
    """
    Predicts the breed of a dog from a base64 encoded image using ResNet50V2.

    Args:
        image_base64_data (str): Base64 encoded image data.

    Returns:
        tuple: Predicted breed and confidence score (percentage).

    Raises:
        ValueError: If the image cannot be loaded or the base64 data is invalid.
    """
    try:
        # Decode base64 string to bytes
        img_data = base64.b64decode(image_base64_data)
        
        # Convert bytes data to a PIL image
        img = Image.open(BytesIO(img_data))
        img = np.array(img)  # Convert to numpy array (for OpenCV compatibility)
        
        if img is None:
            raise ValueError("Image could not be loaded from base64 data.")
        
        # Resize to 224x224 for ResNet50V2
        img = cv2.resize(img, (224, 224))
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)  # Convert to RGB

        # Preprocess the image for the model
        img_array = image.img_to_array(img_rgb)
        img_array = np.expand_dims(img_array, axis=0)  # Add batch dimension
        img_array = preprocess_input(img_array)  # Normalize image for ResNet50V2

        # Make prediction using the model
        predictions = model.predict(img_array)

        # Decode the top prediction
        decoded_predictions = decode_predictions(predictions, top=1)[0]
        breed = decoded_predictions[0][1]  # Predicted breed label
        confidence = decoded_predictions[0][2] * 100  # Confidence score in percentage

        return breed, confidence

    except Exception as e:
        raise ValueError(f"Error processing image: {e}")

if __name__ == "__main__":
    # Use the base64 encoded image data from the imported variable
    image_data = image_base64  # This is the base64 encoded image data imported from data.py

    try:
        breed, confidence = predict_breed_from_base64(image_data)
        print(f"Predicted Breed: {breed}")
        print(f"Confidence: {confidence:.2f}%")
    except ValueError as val_error:
        print(val_error)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")