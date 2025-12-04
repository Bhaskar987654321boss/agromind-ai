import os
import zipfile

MAX_ZIP_SIZE = 90 * 1024 * 1024 # 90MB limit per zip file

def split_file(file_path, chunk_size=50 * 1024 * 1024): # 50MB chunks
    parts = []
    with open(file_path, 'rb') as f:
        part_num = 0
        while True:
            chunk = f.read(chunk_size)
            if not chunk:
                break
            part_name = f"{file_path}.part{part_num}"
            with open(part_name, 'wb') as part_file:
                part_file.write(chunk)
            parts.append(part_name)
            part_num += 1
    return parts

def get_current_zip(zip_num):
    return f"deploy_part_{zip_num}.zip"

def prepare_deployment():
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    excludes = {
        '__pycache__', '.git', '.gitignore', '.env', 'venv', 'env', 
        '.idea', '.vscode', 'db.sqlite3', 'staticfiles', 
        'zip_project.py', 'prepare_deployment.py', 'reassemble.py', '.gemini'
    }

    temp_files = []
    files_to_zip = []

    # 1. Collect all files and split large ones
    for root, dirs, files in os.walk(project_root):
        dirs[:] = [d for d in dirs if d not in excludes]
        
        for file in files:
            if file in excludes or file.endswith('.pyc') or file.startswith('deploy_part_'):
                continue
            
            file_path = os.path.join(root, file)
            file_size = os.path.getsize(file_path)
            
            if file_size > 50 * 1024 * 1024:
                print(f"Splitting large file: {file}")
                parts = split_file(file_path)
                temp_files.extend(parts)
                for part in parts:
                    arcname = os.path.relpath(part, project_root)
                    files_to_zip.append((part, arcname, os.path.getsize(part)))
            else:
                arcname = os.path.relpath(file_path, project_root)
                files_to_zip.append((file_path, arcname, file_size))
    
    # Add reassemble.py manually to the first zip
    files_to_zip.insert(0, ('reassemble.py', 'reassemble.py', os.path.getsize('reassemble.py')))

    # 2. Create multiple zip files
    zip_num = 1
    current_zip_size = 0
    current_zip_name = get_current_zip(zip_num)
    zipf = zipfile.ZipFile(current_zip_name, 'w', zipfile.ZIP_DEFLATED)
    
    print(f"Creating {current_zip_name}...")

    for file_path, arcname, size in files_to_zip:
        # Check if adding this file would exceed the limit
        if current_zip_size + size > MAX_ZIP_SIZE:
            zipf.close()
            zip_num += 1
            current_zip_name = get_current_zip(zip_num)
            current_zip_size = 0
            zipf = zipfile.ZipFile(current_zip_name, 'w', zipfile.ZIP_DEFLATED)
            print(f"Creating {current_zip_name}...")
        
        print(f"  Adding {arcname}")
        zipf.write(file_path, arcname)
        current_zip_size += size

    zipf.close()

    # Clean up temp files
    print("Cleaning up temporary split files...")
    for f in temp_files:
        if os.path.exists(f):
            os.remove(f)

if __name__ == "__main__":
    prepare_deployment()
    print("Deployment files created! Upload ALL deploy_part_*.zip files to PythonAnywhere.")
