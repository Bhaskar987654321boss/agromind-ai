import os
import glob

def reassemble_files():
    # Find all files that have .part0 suffix
    split_files = glob.glob('**/*.part0', recursive=True)
    
    for first_part in split_files:
        base_name = first_part[:-6] # Remove .part0
        print(f"Reassembling {base_name}...")
        
        with open(base_name, 'wb') as outfile:
            part_num = 0
            while True:
                part_name = f"{base_name}.part{part_num}"
                if not os.path.exists(part_name):
                    break
                
                print(f"  - Adding {part_name}")
                with open(part_name, 'rb') as infile:
                    outfile.write(infile.read())
                
                # Optional: Delete part after merging to save space
                os.remove(part_name)
                part_num += 1
        
        print(f"Finished {base_name}")

if __name__ == "__main__":
    print("Starting reassembly of large files...")
    reassemble_files()
    print("Done! You can now proceed with the deployment guide.")
