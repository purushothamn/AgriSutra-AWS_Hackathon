"""
Script to save the AgriSutra logo to the assets folder.

Instructions:
1. Save your logo image as 'agrisutra_logo.png' in the project root
2. Run this script: python save_logo.py
3. The logo will be copied to assets/logo.png
"""

import shutil
import os

def save_logo():
    """Copy logo to assets folder"""
    source = "agrisutra_logo.png"  # Your logo file
    destination = "assets/logo.png"
    
    if not os.path.exists(source):
        print(f"❌ Logo file '{source}' not found!")
        print("\nPlease:")
        print("1. Save your logo image as 'agrisutra_logo.png' in the project root")
        print("2. Run this script again")
        return False
    
    # Create assets folder if it doesn't exist
    os.makedirs("assets", exist_ok=True)
    
    # Copy the logo
    shutil.copy2(source, destination)
    print(f"✅ Logo saved to {destination}")
    print("\nYou can now run your Streamlit app:")
    print("streamlit run app.py")
    return True

if __name__ == "__main__":
    save_logo()
