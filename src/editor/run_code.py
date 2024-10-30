import os
import subprocess

def run_python(code, input_data, temp_dir):
    file_path = os.path.join(temp_dir, 'script.py')
    with open(file_path, 'w') as f:
        f.write(code)
    
    try:
        process = subprocess.run(
            ['python', file_path],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=5
        )
        return process.stderr if process.stderr else process.stdout
    except subprocess.TimeoutExpired:
        return "Error: Program execution timed out (5 seconds)"

def run_cpp(code, input_data, temp_dir):
    source_path = os.path.join(temp_dir, 'program.cpp')
    exe_path = os.path.join(temp_dir, 'program')
    
    with open(source_path, 'w') as f:
        f.write(code)
    
    try:
        # Compile
        compile_process = subprocess.run(
            ['g++', source_path, '-o', exe_path],
            capture_output=True,
            text=True
        )
        if compile_process.returncode != 0:
            return f"Compilation Error:\n{compile_process.stderr}"
        
        # Run
        run_process = subprocess.run(
            [exe_path],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=5
        )
        return run_process.stderr if run_process.stderr else run_process.stdout
    except subprocess.TimeoutExpired:
        return "Error: Program execution timed out (5 seconds)"

def run_java(code, input_data, temp_dir):
    # Extract public class name from code
    import re
    class_match = re.search(r'public\s+class\s+(\w+)', code)
    if not class_match:
        return "Error: No public class found in Java code"
    
    class_name = class_match.group(1)
    source_path = os.path.join(temp_dir, f'{class_name}.java')
    
    with open(source_path, 'w') as f:
        f.write(code)
    
    try:
        # Compile
        compile_process = subprocess.run(
            ['javac', source_path],
            capture_output=True,
            text=True
        )
        if compile_process.returncode != 0:
            return f"Compilation Error:\n{compile_process.stderr}"
        
        # Run
        run_process = subprocess.run(
            ['java', '-cp', temp_dir, class_name],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=5
        )
        return run_process.stderr if run_process.stderr else run_process.stdout
    except subprocess.TimeoutExpired:
        return "Error: Program execution timed out (5 seconds)"

def run_javascript(code, input_data, temp_dir):
    file_path = os.path.join(temp_dir, 'script.js')
    with open(file_path, 'w') as f:
        f.write(code)
    
    try:
        process = subprocess.run(
            ['node', file_path],
            input=input_data,
            capture_output=True,
            text=True,
            timeout=5
        )
        return process.stderr if process.stderr else process.stdout
    except subprocess.TimeoutExpired:
        return "Error: Program execution timed out (5 seconds)"