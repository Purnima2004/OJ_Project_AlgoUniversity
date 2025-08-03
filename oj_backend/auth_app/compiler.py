import subprocess
import tempfile
import os
import time
import uuid
from pathlib import Path

class CodeCompiler:
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp()
        
    def compile_and_run(self, code, language, input_data=""):
        """
        Compile and run code for the given language
        Returns: dict with output, error, execution_time, status
        """
        try:
            if language == 'python':
                return self._run_python(code, input_data)
            elif language == 'cpp':
                return self._run_cpp(code, input_data)
            elif language == 'java':
                return self._run_java(code, input_data)
            else:
                return {
                    'output': '',
                    'error': f'Unsupported language: {language}',
                    'execution_time': 0,
                    'status': 'error'
                }
        except Exception as e:
            return {
                'output': '',
                'error': f'Compilation error: {str(e)}',
                'execution_time': 0,
                'status': 'error'
            }
    
    def _run_python(self, code, input_data):
        """Run Python code"""
        try:
            # Create unique filename
            filename = f"code_{uuid.uuid4().hex}.py"
            filepath = os.path.join(self.temp_dir, filename)
            
            # Write code to file
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Prepare input
            input_bytes = input_data.encode() if input_data else b''
            
            # Run the code
            start_time = time.time()
            result = subprocess.run(
                ['python', filepath],
                input=input_bytes,
                capture_output=True,
                text=True,
                timeout=10,  # 10 second timeout
                cwd=self.temp_dir
            )
            execution_time = time.time() - start_time
            
            # Clean up
            os.remove(filepath)
            
            if result.returncode == 0:
                return {
                    'output': result.stdout,
                    'error': result.stderr,
                    'execution_time': round(execution_time, 3),
                    'status': 'success'
                }
            else:
                return {
                    'output': '',
                    'error': result.stderr or 'Runtime error',
                    'execution_time': round(execution_time, 3),
                    'status': 'error'
                }
                
        except subprocess.TimeoutExpired:
            return {
                'output': '',
                'error': 'Time limit exceeded (10 seconds)',
                'execution_time': 10,
                'status': 'timeout'
            }
        except Exception as e:
            return {
                'output': '',
                'error': f'Python execution error: {str(e)}',
                'execution_time': 0,
                'status': 'error'
            }
    
    def _run_cpp(self, code, input_data):
        """Compile and run C++ code"""
        try:
            # Create unique filenames
            base_name = f"code_{uuid.uuid4().hex}"
            cpp_file = os.path.join(self.temp_dir, f"{base_name}.cpp")
            exe_file = os.path.join(self.temp_dir, f"{base_name}.exe")
            
            # Write code to file
            with open(cpp_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Compile the code
            compile_result = subprocess.run(
                ['g++', '-o', exe_file, cpp_file],
                capture_output=True,
                text=True,
                timeout=10
            )
            
            if compile_result.returncode != 0:
                return {
                    'output': '',
                    'error': f'Compilation error:\n{compile_result.stderr}',
                    'execution_time': 0,
                    'status': 'compilation_error'
                }
            
            # Prepare input
            input_bytes = input_data.encode() if input_data else b''
            
            # Run the compiled program
            start_time = time.time()
            run_result = subprocess.run(
                [exe_file],
                input=input_bytes,
                capture_output=True,
                text=True,
                timeout=10,
                cwd=self.temp_dir
            )
            execution_time = time.time() - start_time
            
            # Clean up
            os.remove(cpp_file)
            if os.path.exists(exe_file):
                os.remove(exe_file)
            
            if run_result.returncode == 0:
                return {
                    'output': run_result.stdout,
                    'error': run_result.stderr,
                    'execution_time': round(execution_time, 3),
                    'status': 'success'
                }
            else:
                return {
                    'output': '',
                    'error': run_result.stderr or 'Runtime error',
                    'execution_time': round(execution_time, 3),
                    'status': 'error'
                }
                
        except subprocess.TimeoutExpired:
            return {
                'output': '',
                'error': 'Time limit exceeded (10 seconds)',
                'execution_time': 10,
                'status': 'timeout'
            }
        except Exception as e:
            return {
                'output': '',
                'error': f'C++ execution error: {str(e)}',
                'execution_time': 0,
                'status': 'error'
            }
    
    def _run_java(self, code, input_data):
        """Compile and run Java code"""
        try:
            # Create unique filenames
            base_name = f"Code_{uuid.uuid4().hex}"
            java_file = os.path.join(self.temp_dir, f"{base_name}.java")
            class_file = os.path.join(self.temp_dir, f"{base_name}.class")
            
            # Write code to file
            with open(java_file, 'w', encoding='utf-8') as f:
                f.write(code)
            
            # Compile the code
            compile_result = subprocess.run(
                ['javac', java_file],
                capture_output=True,
                text=True,
                timeout=10,
                cwd=self.temp_dir
            )
            
            if compile_result.returncode != 0:
                return {
                    'output': '',
                    'error': f'Compilation error:\n{compile_result.stderr}',
                    'execution_time': 0,
                    'status': 'compilation_error'
                }
            
            # Prepare input
            input_bytes = input_data.encode() if input_data else b''
            
            # Run the compiled program
            start_time = time.time()
            run_result = subprocess.run(
                ['java', base_name],
                input=input_bytes,
                capture_output=True,
                text=True,
                timeout=10,
                cwd=self.temp_dir
            )
            execution_time = time.time() - start_time
            
            # Clean up
            os.remove(java_file)
            if os.path.exists(class_file):
                os.remove(class_file)
            
            if run_result.returncode == 0:
                return {
                    'output': run_result.stdout,
                    'error': run_result.stderr,
                    'execution_time': round(execution_time, 3),
                    'status': 'success'
                }
            else:
                return {
                    'output': '',
                    'error': run_result.stderr or 'Runtime error',
                    'execution_time': round(execution_time, 3),
                    'status': 'error'
                }
                
        except subprocess.TimeoutExpired:
            return {
                'output': '',
                'error': 'Time limit exceeded (10 seconds)',
                'execution_time': 10,
                'status': 'timeout'
            }
        except Exception as e:
            return {
                'output': '',
                'error': f'Java execution error: {str(e)}',
                'execution_time': 0,
                'status': 'error'
            }
    
    def cleanup(self):
        """Clean up temporary files"""
        try:
            import shutil
            shutil.rmtree(self.temp_dir)
        except:
            pass 