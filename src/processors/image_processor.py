### Importing the libaries for image processing

import cv2
import numpy
import tensorflow as tf
from PIL import Image
import os

class ImageHandler:
    
    def validate_format(self, path):
        valid_exts = ['.jpg', '.jpeg', '.png', '.bmp', '.tiff']
        _, ext = os.path.splitext(path)
        if ext.lower() not in valid_exts:
            raise ValueError(f"Invalid file extension: {ext}")

    def load_image(self, path):
        # 1. Check if file exists
        if not os.path.exists(path):
            raise FileNotFoundError(f"File not found: {path}")

        # 2. Validate format
        self.validate_format(path)

        # 3. Load image
        img = cv2.imread(path)

        # 4. specific check: OpenCV returns None if it fails to decode
        if img is None:
            raise ValueError("Could not decode image. File might be corrupted.")

        return img

    def save_image(self, img, path):
        success = cv2.imwrite(path, img)
        if not success:
            raise IOError(f"Failed to save image to {path}")

    def resize_image(self, img, max_dim=1280):
        h, w = img.shape[:2]
        
        # Only resize if the image is actually bigger than max_dim
        if max(h, w) > max_dim:
            scale = max_dim / max(h, w)
            new_w = int(w * scale)
            new_h = int(h * scale)
            return cv2.resize(img, (new_w, new_h), interpolation=cv2.INTER_AREA)
            
        return img

    def to_rgb(self, img):
        return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    
    def to_bgr(self, img):
        return cv2.cvtColor(img, cv2.COLOR_RGB2BGR) # This is required while blurring the image when using open cv (The model expects a rgb file)


    def preprocess_for_model(self, path):
    # load correctly
       img = self.load_image(path)

    # resize for model
       img = self.resize_image(img, max_dim=224)

    # convert to RGB for TensorFlow
       img = self.to_rgb(img)

    # normalize
       img = img.astype("float32") / 255.0

       return img


class Image_preprocessor: 
    @staticmethod
    def preprocess(img_rgb, target_size=(128,128), normalization_range='0-1'):
        original_shape = img_rgb.shape[:2]
        resized = tf.image.resize(img_rgb, target_size)

        if normalization_range == '0-1':
            normalized = resized / 255.0
        elif normalization_range == '-1-1':
            normalized = (resized / 127.5) - 1.0  # Fixed: was 'normalization'
        elif normalization_range is None:
            normalized = resized
        else: 
            raise ValueError(f"Invalid Range")
        
        batched = tf.expand_dims(normalized, 0)

        return batched, original_shape
    
    
    def denormalize(img_tensor, normalization_range='0-1'):
        if len(img_tensor.shape) == 4:
            img_tensor = tf.squeeze(img_tensor, 0)

        if normalization_range == '0-1':
            denormalized = img_tensor * 255.0
        elif normalization_range == '-1-1':
            denormalized = (img_tensor + 1.0) * 127.5  # Fixed: was 'denormalization'
        else:
            denormalized = img_tensor

        denormalized = tf.clip_by_value(denormalized, 0, 255)
        denormalized = tf.cast(denormalized, tf.uint8)

        return denormalized.numpy()