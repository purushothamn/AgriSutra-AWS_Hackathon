"""
Test runner script for AgriSutra

Runs all unit tests and displays results.
"""

import subprocess
import sys


def run_tests():
    """Run all unit tests"""
    print("=" * 60)
    print("Running AgriSutra Unit Tests")
    print("=" * 60)
    print()
    
    # Run pytest with verbose output
    # Use python -m pytest for better cross-platform compatibility
    result = subprocess.run(
        [sys.executable, "-m", "pytest", "tests/unit/", "-v", "--tb=short"],
        capture_output=False
    )
    
    print()
    print("=" * 60)
    
    if result.returncode == 0:
        print("✓ All tests passed!")
    else:
        print("✗ Some tests failed. Please review the output above.")
    
    print("=" * 60)
    
    return result.returncode


if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)
