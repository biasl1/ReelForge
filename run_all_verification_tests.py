#!/usr/bin/env python3
"""
Final verification script that runs all tests to confirm the window resize bug fix
and that all other features are preserved.
"""

import sys
import os
import subprocess

def run_test(test_script, description):
    """Run a test script and return success status."""
    print(f"\n{'='*60}")
    print(f"RUNNING: {description}")
    print(f"Script: {test_script}")
    print('='*60)
    
    try:
        result = subprocess.run([sys.executable, test_script], 
                              capture_output=True, text=True, timeout=30)
        
        # Print the output
        if result.stdout:
            print(result.stdout)
        if result.stderr:
            print("STDERR:", result.stderr)
        
        success = result.returncode == 0
        print(f"\nResult: {'✅ PASSED' if success else '❌ FAILED'}")
        return success
        
    except subprocess.TimeoutExpired:
        print("❌ FAILED: Test timed out")
        return False
    except Exception as e:
        print(f"❌ FAILED: Exception occurred: {e}")
        return False

def main():
    """Run all verification tests."""
    print("🚀 STARTING COMPREHENSIVE VERIFICATION SUITE")
    print("Verifying that the window resize bug is fixed and all features work")
    
    # Change to the correct directory
    os.chdir("/Users/test/Documents/development/Artists in DSP/ReelTune")
    
    # List of tests to run
    tests = [
        ("test_content_type_independence.py", "Content Type Independence"),
        ("test_relative_positioning.py", "Relative Positioning During Frame Resize"),
        ("test_zoom_pan_unconstrained.py", "Zoom, Pan, and Unconstrained Placement"),
        ("test_position_persistence.py", "Position Persistence and Save/Load"),
        ("test_window_resize.py", "Window Resize Handling"),
    ]
    
    results = []
    
    # Run each test
    for test_script, description in tests:
        success = run_test(test_script, description)
        results.append((description, success))
    
    # Print final summary
    print(f"\n{'='*80}")
    print("FINAL VERIFICATION RESULTS")
    print('='*80)
    
    all_passed = True
    for description, success in results:
        status = "✅ PASSED" if success else "❌ FAILED"
        print(f"{description:50} {status}")
        if not success:
            all_passed = False
    
    print('='*80)
    if all_passed:
        print("🎉 ALL TESTS PASSED!")
        print("✅ Window resize bug is FIXED")
        print("✅ All features preserved and working correctly")
        print("✅ Modular refactoring successful")
        print("🔥 REELTUNE AI TEMPLATE EDITOR IS READY! 🔥")
    else:
        print("💥 SOME TESTS FAILED!")
        print("❌ Please investigate failed tests")
    print('='*80)
    
    return all_passed

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
