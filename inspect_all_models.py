
import os
import tensorflow as tf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def inspect_models():
    models = ['ml_engine/models/plant_disease_model.h5', 
              'ml_engine/models/rice_model.h5', 
              'ml_engine/models/wheat_model.h5']
    
    for m in models:
        print(f"\nChecking {m}...")
        if not os.path.exists(m):
            print("File not found.")
            continue
            
        try:
            model = tf.keras.models.load_model(m)
            print(f"Output Shape: {model.output_shape}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    inspect_models()
