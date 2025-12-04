from PIL import Image
import os

# Source image path (from the artifact directory)
source_path = r"C:/Users/arunk/.gemini/antigravity/brain/3c107fcb-d3df-4ba0-b167-13b802ca3789/app_icon_1764607906235.png"
dest_dir = r"c:/Users/arunk/OneDrive/Desktop/crp new/static/images/icons"

if not os.path.exists(dest_dir):
    os.makedirs(dest_dir)

try:
    with Image.open(source_path) as img:
        # Save 192x192
        img_192 = img.resize((192, 192), Image.Resampling.LANCZOS)
        img_192.save(os.path.join(dest_dir, "icon-192x192.png"))
        print("Saved icon-192x192.png")

        # Save 512x512
        img_512 = img.resize((512, 512), Image.Resampling.LANCZOS)
        img_512.save(os.path.join(dest_dir, "icon-512x512.png"))
        print("Saved icon-512x512.png")
except Exception as e:
    print(f"Error: {e}")
