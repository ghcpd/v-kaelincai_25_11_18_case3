"""
Validation Script - Verify Project Setup
Quick check to ensure all files are in place and imports work.
"""

import os
import sys


def check_file_exists(filepath, description):
    """Check if a file exists."""
    exists = os.path.exists(filepath)
    status = "✓" if exists else "✗"
    print(f"  {status} {description}: {filepath}")
    return exists


def check_directory_exists(dirpath, description):
    """Check if a directory exists."""
    exists = os.path.isdir(dirpath)
    status = "✓" if exists else "✗"
    print(f"  {status} {description}: {dirpath}")
    return exists


def check_imports():
    """Check if all required packages can be imported."""
    print("\n" + "=" * 80)
    print("CHECKING PYTHON IMPORTS")
    print("=" * 80)
    
    imports = [
        ("PIL", "Pillow (Image processing)"),
        ("cv2", "OpenCV (Computer vision)"),
        ("numpy", "NumPy (Numerical computing)"),
    ]
    
    all_good = True
    for module, description in imports:
        try:
            __import__(module)
            print(f"  ✓ {description}: {module}")
        except ImportError:
            print(f"  ✗ {description}: {module} - NOT INSTALLED")
            all_good = False
    
    return all_good


def main():
    """Run validation checks."""
    print("=" * 80)
    print("UI/UX OPTIMIZATION PIPELINE - VALIDATION")
    print("=" * 80)
    
    all_checks = []
    
    # Check project structure
    print("\n" + "=" * 80)
    print("CHECKING PROJECT STRUCTURE")
    print("=" * 80)
    
    all_checks.append(check_file_exists("README.md", "README file"))
    all_checks.append(check_file_exists("QUICKSTART.md", "Quick start guide"))
    all_checks.append(check_file_exists("requirements.txt", "Requirements file"))
    all_checks.append(check_file_exists("setup.sh", "Setup script (Linux/Mac)"))
    all_checks.append(check_file_exists("setup.ps1", "Setup script (Windows)"))
    all_checks.append(check_file_exists("run_tests.sh", "Run script (Linux/Mac)"))
    all_checks.append(check_file_exists("run_tests.ps1", "Run script (Windows)"))
    all_checks.append(check_file_exists("Dockerfile", "Docker configuration"))
    all_checks.append(check_file_exists("main.py", "Main pipeline script"))
    
    # Check source files
    print("\n" + "=" * 80)
    print("CHECKING SOURCE FILES")
    print("=" * 80)
    
    all_checks.append(check_file_exists("src/image_generator.py", "Image generator"))
    all_checks.append(check_file_exists("src/image_optimizer.py", "Image optimizer"))
    
    # Check test files
    print("\n" + "=" * 80)
    print("CHECKING TEST FILES")
    print("=" * 80)
    
    all_checks.append(check_file_exists("tests/test_pipeline.py", "Test suite"))
    
    # Check directories
    print("\n" + "=" * 80)
    print("CHECKING DIRECTORIES")
    print("=" * 80)
    
    all_checks.append(check_directory_exists("images_original", "Original images folder"))
    all_checks.append(check_directory_exists("images_optimized", "Optimized images folder"))
    all_checks.append(check_directory_exists("images_comparison", "Comparison images folder"))
    all_checks.append(check_directory_exists("results", "Results folder"))
    
    # Check Python imports
    import_check = check_imports()
    
    # Summary
    print("\n" + "=" * 80)
    print("VALIDATION SUMMARY")
    print("=" * 80)
    
    passed = sum(all_checks)
    total = len(all_checks)
    
    print(f"\nFile/Directory Checks: {passed}/{total} passed")
    print(f"Import Checks: {'All passed' if import_check else 'Some failed - run setup.sh/setup.ps1'}")
    
    if passed == total and import_check:
        print("\n✓ ALL VALIDATION CHECKS PASSED!")
        print("\nYou can now run the pipeline:")
        print("  Windows: .\\run_tests.ps1")
        print("  Linux/Mac: bash run_tests.sh")
        return True
    else:
        print("\n✗ SOME VALIDATION CHECKS FAILED")
        if not import_check:
            print("\nTo fix import errors, run:")
            print("  Windows: .\\setup.ps1")
            print("  Linux/Mac: bash setup.sh")
        return False
    
    print("=" * 80)


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
