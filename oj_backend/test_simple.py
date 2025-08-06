#!/usr/bin/env python
"""
Simple test for the compiler
"""
import os
import sys
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'oj_backend.settings')
django.setup()

from auth_app.compiler import CodeCompiler

def test_simple_python():
    """Test simple Python code execution"""
    print("=== Testing Simple Python Code ===")
    
    # Simple test code
    test_code = """
print("Hello, World!")
"""
    
    # Test input
    test_input = ""
    
    # Create compiler
    compiler = CodeCompiler()
    
    try:
        # Test compilation and execution
        result = compiler.compile_and_run(test_code, "python", test_input)
        
        print(f"Result: {result}")
        print(f"Status: {result.get('status')}")
        print(f"Output: '{result.get('output', '')}'")
        print(f"Error: '{result.get('error', '')}'")
        
        if result.get('status') == 'success':
            print("✅ Python compilation and execution successful!")
        else:
            print("❌ Python compilation/execution failed!")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    finally:
        compiler.cleanup()

def test_two_sum_input():
    """Test Two Sum input format"""
    print("\n=== Testing Two Sum Input Format ===")
    
    # Two Sum solution
    test_code = """
def two_sum(nums, target):
    num_to_index = {}
    for i, num in enumerate(nums):
        complement = target - num
        if complement in num_to_index:
            return [num_to_index[complement], i]
        num_to_index[num] = i
    return []

# Read input
first_line = input().split()
n = int(first_line[0])
nums = [int(first_line[i]) for i in range(1, n + 1)]
target = int(input())

# Solve and print result
result = two_sum(nums, target)
print(result[0], result[1])
"""
    
    # Test input (first test case)
    test_input = "4 2 7 11 15\n9"
    
    # Create compiler
    compiler = CodeCompiler()
    
    try:
        # Test compilation and execution
        result = compiler.compile_and_run(test_code, "python", test_input)
        
        print(f"Result: {result}")
        print(f"Status: {result.get('status')}")
        print(f"Output: '{result.get('output', '')}'")
        print(f"Error: '{result.get('error', '')}'")
        
        if result.get('status') == 'success':
            print("✅ Two Sum test successful!")
        else:
            print("❌ Two Sum test failed!")
            
    except Exception as e:
        print(f"❌ Exception: {str(e)}")
    finally:
        compiler.cleanup()

if __name__ == "__main__":
    test_simple_python()
    test_two_sum_input() 