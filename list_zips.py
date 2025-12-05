
import zipfile
import os

zip_files = [f for f in os.listdir('.') if f.startswith('deploy_part_') and f.endswith('.zip')]
zip_files.sort()

print(f"Found zip files: {zip_files}")

for zf in zip_files:
    print(f"\n--- Contents of {zf} ---")
    try:
        with zipfile.ZipFile(zf, 'r') as z:
            # List only first 10 files to avoid flood
            names = z.namelist()
            for name in names[:10]:
                print(name)
            if len(names) > 10:
                print(f"... and {len(names)-10} more files.")
            
            # Check for model file specifically
            if 'ml_engine/models/plant_disease_model.h5' in names:
                print(f"!!! FOUND TARGET MODEL IN {zf} !!!")
                info = z.getinfo('ml_engine/models/plant_disease_model.h5')
                print(f"Size: {info.file_size/1024/1024:.2f} MB")
            elif 'plant_disease_model.h5' in names:
                print(f"!!! FOUND TARGET MODEL IN ROOT OF {zf} !!!")
                info = z.getinfo('plant_disease_model.h5')
                print(f"Size: {info.file_size/1024/1024:.2f} MB")
                
    except Exception as e:
        print(f"Error reading {zf}: {e}")
