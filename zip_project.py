import os
import zipfile

def zip_project(output_filename):
    # Get the directory of the script (project root)
    project_root = os.path.dirname(os.path.abspath(__file__))
    
    # Files/Dirs to exclude
    excludes = {
        '__pycache__', '.git', '.gitignore', '.env', 'venv', 'env', 
        '.idea', '.vscode', 'db.sqlite3', 'staticfiles', 
        output_filename, 'zip_project.py', '.gemini',
        'ml_engine/models' # Exclude large models
    }

    with zipfile.ZipFile(output_filename, 'w', zipfile.ZIP_DEFLATED) as zipf:
        for root, dirs, files in os.walk(project_root):
            # Modify dirs in-place to skip excluded directories
            dirs[:] = [d for d in dirs if d not in excludes]
            
            for file in files:
                if file in excludes or file.endswith('.pyc'):
                    continue
                
                file_path = os.path.join(root, file)
                # Archive name should be relative to project root
                arcname = os.path.relpath(file_path, project_root)
                
                print(f"Adding {arcname}")
                zipf.write(file_path, arcname)

if __name__ == "__main__":
    zip_project('project_upload.zip')
    print("Zip file created successfully!")
