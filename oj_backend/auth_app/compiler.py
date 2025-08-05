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
        "python": ["python3", "-B"],  # -B prevents writing .pyc files
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
            
            # Map language to proper file extension
            extensions = {
                "cpp": "cpp",
                "java": "java", 
                "python": "py"
            }
            extension = extensions.get(language, language)
            code_file = Path(self.temp_dir) / "codes" / f"{unique_id}.{extension}"
            
            # Write code to file
            with open(code_file, "w", encoding='utf-8') as f:
                f.write(code)
            
            result = {}
            
            if language == "cpp":
                result = self._run_cpp(code_file, unique_id, input_data)
            elif language == "java":
                result = self._run_java(code_file, unique_id, input_data)
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
        finally:
            self.cleanup()

    def _run_cpp(self, code_file: Path, unique_id: str, 
                input_data: str) -> Dict[str, Any]:
        """Compile and run C++ code"""
        executable = Path(self.temp_dir) / "codes" / f"{unique_id}.exe"
        
        # Compile
        compile_cmd = [*self.COMPILE_OPTIONS["cpp"], 
                      str(code_file), "-o", str(executable)]
        compile_result = self._secure_run(compile_cmd)
        
        if compile_result['returncode'] != 0:
            return {
                'output': '',
                'error': f"Compilation error:\n{compile_result['error']}",
                'execution_time': 0,
                'status': 'compilation_error'
            }
        
        # Prepare input - ensure it ends with newline for proper input handling
        if input_data and not input_data.endswith('\n'):
            input_data += '\n'
        
        # If no input provided, create a simple input to prevent hanging
        if not input_data.strip():
            input_data = '1 2\n'  # Default input to prevent hanging
       
        
        # Run
        start_time = time.time()
        run_result = self._secure_run([str(executable)], input_data)
        execution_time = time.time() - start_time
        
        return {
            'output': run_result['output'],
            'error': run_result['error'],
            'execution_time': round(execution_time, 3),
            'status': 'success' if run_result['returncode'] == 0 else 'error'
        }

    def _run_java(self, code_file: Path, unique_id: str, 
                 input_data: str) -> Dict[str, Any]:
        """Compile and run Java code"""
        class_file = Path(self.temp_dir) / "codes" / f"{unique_id}.class"
        
        # Compile
        compile_cmd = [*self.COMPILE_OPTIONS["java"], str(code_file)]
        compile_result = self._secure_run(compile_cmd)
        
        if compile_result['returncode'] != 0:
            return {
                'output': '',
                'error': f"Compilation error:\n{compile_result['error']}",
                'execution_time': 0,
                'status': 'compilation_error'
            }
        
        # Prepare input - ensure it ends with newline for proper input handling
        if input_data and not input_data.endswith('\n'):
            input_data += '\n'
        
        # If no input provided, create a simple input to prevent hanging
        if not input_data.strip():
            input_data = '1 2\n'  # Default input to prevent hanging
        
        
        # Run
        start_time = time.time()
        run_cmd = ['java', '-cp', str(Path(self.temp_dir) / "codes"), unique_id]
        run_result = self._secure_run(run_cmd, input_data)
        execution_time = time.time() - start_time
        
        return {
            'output': run_result['output'],
            'error': run_result['error'],
            'execution_time': round(execution_time, 3),
            'status': 'success' if run_result['returncode'] == 0 else 'error'
        }

    def _run_python(self, code_file: Path, input_data: str) -> Dict[str, Any]:
        """Run Python code"""
        # Prepare input - ensure it ends with newline for proper input handling
        if input_data and not input_data.endswith('\n'):
            input_data += '\n'
        
        # If no input provided, create a simple input to prevent hanging
        if not input_data.strip():
            input_data = '1 2\n'  # Default input to prevent hanging
  
        
        run_cmd = [*self.COMPILE_OPTIONS["python"], str(code_file)]
        start_time = time.time()
        result = self._secure_run(run_cmd, input_data)
        execution_time = time.time() - start_time
        
        return {
            'output': result['output'],
            'error': result['error'],
            'execution_time': round(execution_time, 3),
            'status': 'success' if result['returncode'] == 0 else 'error'
        }

    def cleanup(self):
        """Clean up temporary files"""
        try:
            import shutil
            shutil.rmtree(self.temp_dir)
        except Exception as e:
            logger.error(f"Cleanup error: {str(e)}") 