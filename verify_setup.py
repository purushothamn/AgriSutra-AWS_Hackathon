"""
Quick verification script to check project setup.
Run this after setup to verify the structure is correct.
"""

import os
import sys

def check_directory(path, name):
    """Check if a directory exists."""
    if os.path.isdir(path):
        print(f"✓ {name} directory exists")
        return True
    else:
        print(f"✗ {name} directory missing")
        return False

def check_file(path, name):
    """Check if a file exists."""
    if os.path.isfile(path):
        print(f"✓ {name} file exists")
        return True
    else:
        print(f"✗ {name} file missing")
        return False

def main():
    """Run verification checks."""
    print("AgriSutra Project Setup Verification")
    print("=" * 50)
    
    all_checks = []
    
    # Check main directories
    print("\nChecking main directories...")
    all_checks.append(check_directory("agrisutra", "agrisutra"))
    all_checks.append(check_directory("tests", "tests"))
    
    # Check agrisutra subdirectories
    print("\nChecking agrisutra subdirectories...")
    all_checks.append(check_directory("agrisutra/voice_pipeline", "voice_pipeline"))
    all_checks.append(check_directory("agrisutra/agents", "agents"))
    all_checks.append(check_directory("agrisutra/safety", "safety"))
    all_checks.append(check_directory("agrisutra/translation", "translation"))
    all_checks.append(check_directory("agrisutra/ui", "ui"))
    
    # Check test subdirectories
    print("\nChecking test subdirectories...")
    all_checks.append(check_directory("tests/unit", "unit tests"))
    all_checks.append(check_directory("tests/properties", "property tests"))
    all_checks.append(check_directory("tests/integration", "integration tests"))
    
    # Check configuration files
    print("\nChecking configuration files...")
    all_checks.append(check_file("agrisutra/config.py", "config.py"))
    all_checks.append(check_file("requirements.txt", "requirements.txt"))
    all_checks.append(check_file(".env.example", ".env.example"))
    all_checks.append(check_file("pytest.ini", "pytest.ini"))
    all_checks.append(check_file("README.md", "README.md"))
    
    # Check setup scripts
    print("\nChecking setup scripts...")
    all_checks.append(check_file("setup.sh", "setup.sh (Linux/Mac)"))
    all_checks.append(check_file("setup.bat", "setup.bat (Windows)"))
    
    # Check __init__ files
    print("\nChecking __init__.py files...")
    all_checks.append(check_file("agrisutra/__init__.py", "agrisutra/__init__.py"))
    all_checks.append(check_file("tests/__init__.py", "tests/__init__.py"))
    
    # Summary
    print("\n" + "=" * 50)
    passed = sum(all_checks)
    total = len(all_checks)
    
    if passed == total:
        print(f"✓ All checks passed ({passed}/{total})")
        print("\nProject structure is set up correctly!")
        print("\nNext steps:")
        print("1. Run setup script: ./setup.sh (Linux/Mac) or setup.bat (Windows)")
        print("2. Configure .env file with your AWS credentials")
        print("3. Run tests: pytest")
        print("4. Start the app: streamlit run app.py")
        return 0
    else:
        print(f"✗ Some checks failed ({passed}/{total})")
        print("\nPlease review the missing items above.")
        return 1

if __name__ == "__main__":
    sys.exit(main())
