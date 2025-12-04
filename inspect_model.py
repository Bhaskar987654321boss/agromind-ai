import os
import sys
import numpy as np
import tensorflow as tf
from PIL import Image

# Suppress TF logs
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def inspect_and_test():
    model_path = 'ml_engine/models/plant_disease_model.h5'
    
    if not os.path.exists(model_path):
        print(f"Model not found at {model_path}")
        return

    try:
        print("Loading model...")
        model = tf.keras.models.load_model(model_path)
        
        print("\n--- Model Input Details ---")
        input_shape = model.input_shape
        print(f"Expected Input Shape: {input_shape}")
        
        # Create a dummy image (random noise)
        # Assuming (256, 256, 3) based on previous code, but we'll check input_shape
        target_h, target_w = 256, 256
        if input_shape and len(input_shape) == 4:
            target_h, target_w = input_shape[1], input_shape[2]
            
        print(f"Testing with dummy image of size: {target_h}x{target_w}")
        
        # Test 1: Black Image
        img_black = np.zeros((1, target_h, target_w, 3), dtype=np.float32)
        pred_black = model.predict(img_black, verbose=0)
        idx_black = np.argmax(pred_black[0])
        conf_black = np.max(pred_black[0])
        print(f"Black Image Prediction: Index {idx_black}, Confidence {conf_black:.4f}")

        # Test 2: White Image (Normalized)
        img_white = np.ones((1, target_h, target_w, 3), dtype=np.float32)
        pred_white = model.predict(img_white, verbose=0)
        idx_white = np.argmax(pred_white[0])
        conf_white = np.max(pred_white[0])
        print(f"White Image Prediction: Index {idx_white}, Confidence {conf_white:.4f}")
        
        # Test 3: Random Noise
        img_noise = np.random.rand(1, target_h, target_w, 3).astype(np.float32)
        pred_noise = model.predict(img_noise, verbose=0)
        idx_noise = np.argmax(pred_noise[0])
        conf_noise = np.max(pred_noise[0])
        print(f"Random Noise Prediction: Index {idx_noise}, Confidence {conf_noise:.4f}")
        
        print("\nIf all predictions are the same (e.g., Index 1), the model might be biased or expecting different preprocessing.")

    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    with open('inspect_result.txt', 'w') as f:
        sys.stdout = f
        inspect_and_test()
