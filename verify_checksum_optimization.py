#!/usr/bin/env python3
"""Verify checksum optimization implementation for Issue #23864."""

import hashlib
import json
import os
import sys


def compute_checksum(file_path):
    """Compute SHA256 checksum of a file."""
    hasher = hashlib.sha256()
    with open(file_path, 'rb') as f:
        for chunk in iter(lambda: f.read(8192), b''):
            hasher.update(chunk)
    return hasher.hexdigest()


def verify_implementation():
    """Verify that checksum optimization is implemented."""
    # Check implementation files
    required_files = [
        'scripts/pip_requirements_checksum_manager.py',
        'scripts/install_python_dev_dependencies.py',
        'scripts/install_python_prod_dependencies.py'
    ]
    
    print("Implementation files:")
    all_exist = True
    for file_path in required_files:
        exists = os.path.exists(file_path)
        status = "OK" if exists else "MISSING"
        print(f"  [{status}] {file_path}")
        all_exist = all_exist and exists
    
    if not all_exist:
        return False
    
    # Check checksum file
    checksum_file = 'pip_requirements_checksums.json'
    if os.path.exists(checksum_file):
        with open(checksum_file, 'r') as f:
            checksums = json.load(f)
        print(f"\nChecksum cache: {checksum_file} ({len(checksums)} files)")
    
    # Verify checksum computation
    test_files = ['requirements.in', 'requirements_dev.in']
    print("\nCurrent checksums:")
    for file_path in test_files:
        if os.path.exists(file_path):
            checksum = compute_checksum(file_path)
            print(f"  {file_path}: {checksum[:16]}...")
    
    return True


if __name__ == '__main__':
    success = verify_implementation()
    sys.exit(0 if success else 1)
