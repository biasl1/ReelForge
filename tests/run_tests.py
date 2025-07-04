#!/usr/bin/env python3
"""
ReelTune Test Runner
Run all tests in the tests directory
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from core.logging_config import log_info, log_error, log_warning

def run_all_tests():
    """Run all available tests"""
    log_info("🚀 Starting ReelTune Test Suite")

    tests_dir = Path(__file__).parent
    test_files = list(tests_dir.glob("test_*.py"))

    log_info(f"Found {len(test_files)} test files")

    passed = 0
    failed = 0

    for test_file in sorted(test_files):
        log_info(f"\n{'='*50}")
        log_info(f"Running: {test_file.name}")
        log_info(f"{'='*50}")

        try:
            # Execute the test file
            exec(open(test_file).read(), {"__file__": str(test_file)})
            passed += 1
            log_info(f"✅ {test_file.name} - PASSED")
        except Exception as e:
            failed += 1
            log_error(f"❌ {test_file.name} - FAILED: {e}")

    log_info(f"\n{'='*50}")
    log_info(f"Test Results: {passed} passed, {failed} failed")
    log_info(f"{'='*50}")

    return failed == 0

if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
