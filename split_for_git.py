import os

def split_file(file_path, chunk_size=50 * 1024 * 1024): # 50MB chunks
    if not os.path.exists(file_path):
        print(f"File not found: {file_path}")
        return

    file_size = os.path.getsize(file_path)
    if file_size < chunk_size:
        print(f"Skipping {file_path} (size {file_size/1024/1024:.2f}MB is smaller than chunk limit)")
        return

    print(f"Splitting {file_path} ({file_size/1024/1024:.2f}MB)...")
    
    with open(file_path, 'rb') as f:
        part_num = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            part_name = f"{file_path}.part{part_num}"
            print(f"  - Creating {part_name}")
            with open(part_name, 'wb') as part_file:
                part_file.write(chunk)
            part_num += 1
    print("Done splitting.")

if __name__ == "__main__":
    # List of large models to check/split
    large_files = [
        'ml_engine/models/rice_model.h5',
        # Add others if they grow > 50MB
    ]
    
    for f in large_files:
        split_file(f)
