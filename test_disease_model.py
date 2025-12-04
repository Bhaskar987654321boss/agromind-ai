import os
import sys
import django
from django.conf import settings

# Setup Django environment
sys.path.append(os.getcwd())
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'crop_project.settings')
django.setup()

from ml_engine.disease_prediction import predictor
import numpy as np
from PIL import Image

def test_prediction():
    print("Testing Disease Prediction Model...")
    
    # 1. Check if model loaded
    if predictor.primary_model:
        print("[PASS] Primary Model Loaded")
    else:
        print("[FAIL] Primary Model NOT Loaded")
        
    # 2. Create a dummy image
    print("Creating dummy image for testing...")
    img = Image.new('RGB', (256, 256), color = 'green')
    img_path = 'test_leaf.jpg'
    img.save(img_path)
    
    # 3. Run prediction
    print("Running prediction on dummy image...")
    try:
        result = predictor.predict_from_image(img_path)
        print("Prediction Result:")
        print(result)
        
        if result.get('disease') and result.get('confidence') is not None:
             print("[PASS] Prediction returned valid structure")
        else:
             print("[FAIL] Prediction returned invalid structure")
             
    except Exception as e:
        print(f"[FAIL] Prediction crashed: {e}")
        
    # Cleanup
    if os.path.exists(img_path):
        os.remove(img_path)

if __name__ == "__main__":
    test_prediction()
