import os
import uuid
import subprocess
import tempfile
import signal
import logging
import time
from pathlib import Path
from typing import Dict, Any

# Import resource module only on Unix/Linux systems
try:
    import resource
    RESOURCE_AVAILABLE = True
except ImportError:
    RESOURCE_AVAILABLE = False

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CompilerError(Exception):
    """Custom exception for compiler related errors"""
    pass

class CodeCompiler:
    """Handles secure code execution with resource limits"""
    
    MEMORY_LIMIT = 512 * 1024 * 1024  # 512MB
    TIME_LIMIT = 10  # seconds
    MAX_OUTPUT_SIZE = 1024 * 1024  # 1MB
    
    COMPILE_OPTIONS = {
        "cpp": ["g++", "-O2", "-std=c++17", "-Wall"],
        "java": ["javac", "-Xlint"],
        "python": ["python", "-B"],  # Use 'python' for Windows compatibility
    }
    
    def __init__(self):
        self.temp_dir = tempfile.mkdtemp(prefix='code_exec_')
        self._setup_directories()
        
    def _setup_directories(self):
        """Create necessary directories with proper permissions"""
        directories = ["codes", "inputs", "outputs"]
        for directory in directories:
            dir_path = Path(self.temp_dir) / directory
            dir_path.mkdir(parents=True, exist_ok=True)
            # Set restrictive permissions
            os.chmod(str(dir_path), 0o700)
    
    def _secure_run(self, cmd: list, input_data: str = None, 
                   timeout: int = TIME_LIMIT) -> Dict[str, Any]:
        """Execute command with security constraints"""
        try:
            # Set up resource limits
            def limit_resources():
                if RESOURCE_AVAILABLE:  # Only on Unix/Linux systems
                    resource.setrlimit(resource.RLIMIT_AS, 
                                     (self.MEMORY_LIMIT, self.MEMORY_LIMIT))
                    resource.setrlimit(resource.RLIMIT_CPU, 
                                     (timeout, timeout))

            result = subprocess.run(
                cmd,
                input=input_data,
                capture_output=True,
                text=True,
                timeout=timeout,
                preexec_fn=limit_resources if RESOURCE_AVAILABLE else None,
                cwd=self.temp_dir
            )
            
            if len(result.stdout) > self.MAX_OUTPUT_SIZE:
                raise CompilerError("Output size exceeded limit")
                
            return {
                'output': result.stdout,
                'error': result.stderr,
                'returncode': result.returncode
            }
            
        except subprocess.TimeoutExpired:
            raise CompilerError("Time limit exceeded")
        except Exception as e:
            raise CompilerError(f"Execution error: {str(e)}")

    def compile_and_run(self, code: str, language: str, input_data: str = "") -> Dict[str, Any]:
        """Main method to compile and run code"""
        try:
            if language not in self.COMPILE_OPTIONS:
                raise CompilerError(f"Unsupported language: {language}")
                
            unique_id = str(uuid.uuid4())
            
            # Create codes directory if it doesn't exist
            codes_dir = Path(self.temp_dir) / "codes"
            codes_dir.mkdir(parents=True, exist_ok=True)

            # Map language to proper file extension
            extensions = {
                "cpp": "cpp",
                "java": "java",
                "python": "py"
            }

            # --- Java class name fix ---
            if language == "java":
                import re
                # Generate a valid Java class name from unique_id
                java_class_name = f"Main_{unique_id.replace('-', '_')}"
                # Replace 'public class <something>' or 'class <something>' with our class name
                code = re.sub(r'(public\s+)?class\s+\w+', f'class {java_class_name}', code)
                extension = "java"
                code_file = codes_dir / f"{java_class_name}.java"
            else:
                extension = extensions.get(language, language)
                code_file = codes_dir / f"{unique_id}.{extension}"
            
            # Write code to file
            with open(code_file, "w", encoding='utf-8') as f:
                f.write(code)
            
            print(f"DEBUG: Created file: {code_file}")
            print(f"DEBUG: File exists: {code_file.exists()}")
            
            result = {}
            
            if language == "cpp":
                result = self._run_cpp(code_file, unique_id, input_data)
            elif language == "java":
                result = self._run_java(code_file, java_class_name, input_data)
            elif language == "python":
                result = self._run_python(code_file, input_data)
                
            return result
            
        except CompilerError as e:
            logger.error(f"Compilation/Execution error: {str(e)}")
            return {
                'output': '',
                'error': str(e),
                'execution_time': 0,
                'status': 'error'
            }
        except Exception as e:
            logger.error(f"Unexpected error: {str(e)}")
            return {
                'output': '',
                'error': f"Unexpected error: {str(e)}",
                'execution_time': 0,
                'status': 'error'
            }

    def _run_cpp(self, code_file: Path, unique_id: str, 
                 input_data: str) -> Dict[str, Any]:
        """Compile and run C++ code"""
        try:
            # Ensure the codes directory exists
            codes_dir = Path(self.temp_dir) / "codes"
            codes_dir.mkdir(parents=True, exist_ok=True)
            
            # Use .exe extension on Windows
            import platform
            if platform.system() == "Windows":
                executable = codes_dir / f"{unique_id}.exe"
            else:
                executable = codes_dir / unique_id
            
            print(f"DEBUG: C++ compilation - code_file: {code_file}")
            print(f"DEBUG: C++ compilation - executable: {executable}")
            print(f"DEBUG: C++ compilation - code_file exists: {code_file.exists()}")
            
            # Try different C++ compiler commands for Windows compatibility
            cpp_commands = ["g++", "g++.exe"]
            
            # Try to compile with different g++ commands
            compile_success = False
            for gpp_cmd in cpp_commands:
                try:
                    compile_cmd = [gpp_cmd, "-O2", "-std=c++17", "-Wall", 
                                  str(code_file), "-o", str(executable)]
                    print(f"DEBUG: Compile command: {compile_cmd}")
                    
                    compile_result = self._secure_run(compile_cmd)
                    print(f"DEBUG: Compile result: {compile_result}")
                    
                    if compile_result['returncode'] == 0:
                        compile_success = True
                        break
                    elif "not found" in compile_result['error'] or "cannot find" in compile_result['error']:
                        # Try next command
                        continue
                    else:
                        # Compilation error, not command not found
                        return {
                            'output': '',
                            'error': f"Compilation error:\n{compile_result['error']}",
                            'execution_time': 0,
                            'status': 'compilation_error'
                        }
                except Exception as e:
                    # Try next command
                    continue
            
            if not compile_success:
                return {
                    'output': '',
                    'error': 'C++ compiler (g++) not found. Please ensure MinGW or similar C++ compiler is installed and added to PATH.',
                    'execution_time': 0,
                    'status': 'compilation_error'
                }
            
            print(f"DEBUG: Executable created: {executable.exists()}")
            
            # Prepare input - ensure it ends with newline for proper input handling
            if input_data and not input_data.endswith('\n'):
                input_data += '\n'
            
            # If no input provided, create a simple input to prevent hanging
            if not input_data.strip():
                input_data = '1 2\n'  # Default input to prevent hanging
            
            print(f"DEBUG: Input data: '{input_data}'")
            
            # Run
            start_time = time.time()
            run_result = self._secure_run([str(executable)], input_data)
            execution_time = time.time() - start_time
            
            print(f"DEBUG: Run result: {run_result}")
            
            # Enhanced error handling for C++
            if run_result['returncode'] == 0:
                return {
                    'output': run_result['output'],
                    'error': run_result['error'],
                    'execution_time': round(execution_time, 3),
                    'status': 'success'
                }
            else:
                # Map return codes to specific error messages
                error_message = self._get_cpp_error_message(run_result['returncode'], run_result['error'])
                return {
                    'output': '',
                    'error': error_message,
                    'execution_time': round(execution_time, 3),
                    'status': 'runtime_error'
                }
        except Exception as e:
            print(f"DEBUG: C++ execution error: {str(e)}")
            return {
                'output': '',
                'error': f"C++ execution error: {str(e)}",
                'execution_time': 0,
                'status': 'error'
            }

    def _run_java(self, code_file: Path, java_class_name: str, 
                 input_data: str) -> Dict[str, Any]:
        """Compile and run Java code"""
        class_file = Path(self.temp_dir) / "codes" / f"{java_class_name}.class"
        
        # Try different Java commands for Windows compatibility
        java_commands = ["javac", "javac.exe"]
        
        # Try to compile with different javac commands
        compile_success = False
        for javac_cmd in java_commands:
            try:
                compile_cmd = [javac_cmd, str(code_file)]
                compile_result = self._secure_run(compile_cmd)
                
                if compile_result['returncode'] == 0:
                    compile_success = True
                    break
                elif "not found" in compile_result['error'] or "cannot find" in compile_result['error']:
                    # Try next command
                    continue
                else:
                    # Compilation error, not command not found
                    return {
                        'output': '',
                        'error': f"Compilation error:\n{compile_result['error']}",
                        'execution_time': 0,
                        'status': 'compilation_error'
                    }
            except Exception as e:
                # Try next command
                continue
        
        if not compile_success:
            return {
                'output': '',
                'error': 'Java compiler (javac) not found. Please ensure Java JDK is installed and added to PATH.',
                'execution_time': 0,
                'status': 'compilation_error'
            }
        
        # Prepare input - ensure it ends with newline for proper input handling
        if input_data and not input_data.endswith('\n'):
            input_data += '\n'
        
        # If no input provided, create a simple input to prevent hanging
        if not input_data.strip():
            input_data = '1 2\n'  # Default input to prevent hanging
        
        # Try different java commands for running
        java_commands = ["java", "java.exe"]
        
        for java_cmd in java_commands:
            try:
                # Run
                start_time = time.time()
                run_cmd = [java_cmd, '-cp', str(Path(self.temp_dir) / "codes"), java_class_name]
                run_result = self._secure_run(run_cmd, input_data)
                execution_time = time.time() - start_time
                
                # Enhanced error handling for Java
                if run_result['returncode'] == 0:
                    return {
                        'output': run_result['output'],
                        'error': run_result['error'],
                        'execution_time': round(execution_time, 3),
                        'status': 'success'
                    }
                else:
                    # Map return codes to specific error messages
                    error_message = self._get_java_error_message(run_result['returncode'], run_result['error'])
                    return {
                        'output': '',
                        'error': error_message,
                        'execution_time': round(execution_time, 3),
                        'status': 'runtime_error'
                    }
            except Exception as e:
                # Try next command
                continue
        
        # If all java commands fail
        return {
            'output': '',
            'error': 'Java runtime (java) not found. Please ensure Java JRE is installed and added to PATH.',
            'execution_time': 0,
            'status': 'error'
        }

    def _run_python(self, code_file: Path, input_data: str) -> Dict[str, Any]:
        """Run Python code"""
        # Prepare input - ensure it ends with newline for proper input handling
        if input_data and not input_data.endswith('\n'):
            input_data += '\n'
        
        # If no input provided, create a simple input to prevent hanging
        if not input_data.strip():
            input_data = '1 2\n'  # Default input to prevent hanging
        
        # Try different Python commands for Windows compatibility
        python_commands = ["python", "python3", "py"]
        
        for python_cmd in python_commands:
            try:
                run_cmd = [python_cmd, "-B", str(code_file)]
                start_time = time.time()
                result = self._secure_run(run_cmd, input_data)
                execution_time = time.time() - start_time
                
                # Enhanced error handling for Python
                if result['returncode'] == 0:
                    return {
                        'output': result['output'],
                        'error': result['error'],
                        'execution_time': round(execution_time, 3),
                        'status': 'success'
                    }
                else:
                    # Map Python errors to specific error messages
                    error_message = self._get_python_error_message(result['error'])
                    return {
                        'output': '',
                        'error': error_message,
                        'execution_time': round(execution_time, 3),
                        'status': 'runtime_error'
                    }
            except Exception as e:
                # If this command fails, try the next one
                continue
        
        # If all commands fail, return an error
        return {
            'output': '',
            'error': 'Python not found. Please ensure Python is installed and added to PATH.',
            'execution_time': 0,
            'status': 'error'
        }

    def _get_cpp_error_message(self, returncode: int, stderr: str) -> str:
        """Map C++ return codes to user-friendly error messages"""
        error_messages = {
            3221225477: "Runtime Error: Memory Access Violation (Segmentation Fault)\n\nThis usually means:\n• Array/vector index out of bounds\n• Accessing null pointer\n• Stack overflow\n• Memory corruption\n\nCheck your code for:\n• Valid array indices\n• Proper pointer initialization\n• Recursion depth limits",
            3221225725: "Runtime Error: Stack Overflow\n\nThis usually means:\n• Infinite recursion\n• Too many local variables\n• Deep function calls\n\nCheck your code for:\n• Recursion base cases\n• Function call depth",
            3221225620: "Runtime Error: Division by Zero\n\nCheck your code for:\n• Division operations\n• Modulo operations\n• Input validation",
            3221225478: "Runtime Error: Invalid Instruction\n\nThis usually means:\n• Corrupted executable\n• Incompatible binary\n\nTry recompiling your code.",
            3221225786: "Runtime Error: Access Violation\n\nThis usually means:\n• Invalid memory access\n• Buffer overflow\n• Uninitialized variables\n\nCheck your code for:\n• Array bounds\n• Variable initialization\n• Memory allocation",
        }
        
        # Check for specific error patterns in stderr
        if "terminate called after throwing an instance of" in stderr:
            return f"Runtime Error: Exception Thrown\n\n{stderr}"
        elif "Aborted" in stderr:
            return f"Runtime Error: Program Aborted\n\n{stderr}"
        elif "Segmentation fault" in stderr:
            return "Runtime Error: Segmentation Fault\n\nThis usually means:\n• Array/vector index out of bounds\n• Accessing null pointer\n• Memory corruption"
        
        # Return specific error message if available, otherwise generic
        return error_messages.get(returncode, f"Runtime Error (Exit Code: {returncode})\n\n{stderr}")

    def _get_java_error_message(self, returncode: int, stderr: str) -> str:
        """Map Java return codes to user-friendly error messages"""
        if "OutOfMemoryError" in stderr:
            return "Runtime Error: Out of Memory\n\nThis usually means:\n• Infinite loops\n• Large data structures\n• Memory leaks\n\nCheck your code for:\n• Loop termination conditions\n• Memory usage patterns"
        elif "ArrayIndexOutOfBoundsException" in stderr:
            return "Runtime Error: Array Index Out of Bounds\n\nThis usually means:\n• Accessing array with invalid index\n• Negative array index\n• Index >= array length\n\nCheck your code for:\n• Array bounds validation\n• Loop conditions"
        elif "NullPointerException" in stderr:
            return "Runtime Error: Null Pointer Exception\n\nThis usually means:\n• Accessing null object\n• Uninitialized object\n\nCheck your code for:\n• Object initialization\n• Null checks"
        elif "StackOverflowError" in stderr:
            return "Runtime Error: Stack Overflow\n\nThis usually means:\n• Infinite recursion\n• Deep function calls\n\nCheck your code for:\n• Recursion base cases\n• Function call depth"
        elif "NumberFormatException" in stderr:
            return "Runtime Error: Number Format Exception\n\nThis usually means:\n• Invalid number parsing\n• Non-numeric input\n\nCheck your code for:\n• Input validation\n• Number parsing"
        else:
            return f"Runtime Error (Exit Code: {returncode})\n\n{stderr}"

    def _get_python_error_message(self, stderr: str) -> str:
        """Map Python errors to user-friendly error messages"""
        if "IndexError" in stderr:
            return "Runtime Error: Index Error\n\nThis usually means:\n• List/array index out of bounds\n• Negative index\n• Empty list access\n\nCheck your code for:\n• List bounds validation\n• List length checks"
        elif "KeyError" in stderr:
            return "Runtime Error: Key Error\n\nThis usually means:\n• Dictionary key not found\n• Invalid dictionary access\n\nCheck your code for:\n• Dictionary key existence\n• Key validation"
        elif "ZeroDivisionError" in stderr:
            return "Runtime Error: Division by Zero\n\nCheck your code for:\n• Division operations\n• Input validation"
        elif "NameError" in stderr:
            return "Runtime Error: Name Error\n\nThis usually means:\n• Undefined variable\n• Typo in variable name\n\nCheck your code for:\n• Variable declaration\n• Variable name spelling"
        elif "TypeError" in stderr:
            return "Runtime Error: Type Error\n\nThis usually means:\n• Wrong data type operation\n• Invalid function arguments\n\nCheck your code for:\n• Data type compatibility\n• Function parameter types"
        elif "ValueError" in stderr:
            return "Runtime Error: Value Error\n\nThis usually means:\n• Invalid value for operation\n• Wrong input format\n\nCheck your code for:\n• Input validation\n• Value ranges"
        elif "MemoryError" in stderr:
            return "Runtime Error: Memory Error\n\nThis usually means:\n• Out of memory\n• Large data structures\n\nCheck your code for:\n• Memory usage\n• Data structure size"
        elif "RecursionError" in stderr:
            return "Runtime Error: Recursion Error\n\nThis usually means:\n• Maximum recursion depth exceeded\n• Infinite recursion\n\nCheck your code for:\n• Recursion base cases\n• Recursion depth limits"
        else:
            return f"Runtime Error:\n\n{stderr}"

    def cleanup(self):
        """Clean up temporary files"""
        try:
            import shutil
            shutil.rmtree(self.temp_dir)
        except Exception as e:
            logger.error(f"Cleanup error: {str(e)}") 