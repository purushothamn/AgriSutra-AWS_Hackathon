"""
Clear Python cache files to fix import issues
"""

import os
import shutil

def clear_pycache():
    """Remove all __pycache__ directories"""
    count = 0
    for root, dirs, files in os.walk('.'):
        if '__pycache__' in dirs:
            pycache_path = os.path.join(root, '__pycache__')
            print(f"Removing: {pycache_path}")
            shutil.rmtree(pycache_path)
            count += 1
    
    print(f"\n✅ Cleared {count} __pycache__ directories")
    print("🔄 Please restart your Streamlit app now")

if __name__ == "__main__":
    clear_pycache()
