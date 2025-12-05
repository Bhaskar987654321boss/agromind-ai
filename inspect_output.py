
import os
import sys
import tensorflow as tf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

def inspect_output_shape():
    model_path = 'ml_engine/models/plant_disease_model.h5'
    try:
        model = tf.keras.models.load_model(model_path)
        output_shape = model.output_shape
        print(f"Model Output Shape: {output_shape}")
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    inspect_output_shape()
