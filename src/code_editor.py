from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QPlainTextEdit, QComboBox
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, pyqtSlot, QObject
from PyQt5.QtWebChannel import QWebChannel
import os
import subprocess
import tempfile
import shutil

class WebChannel(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)
        
    @pyqtSlot(str, result=str)
    def get_code(self, code):
        self.parent().current_code = code
        return "ok"

class CodeEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.current_code = ""
        self.current_language = "python"
        self.language_commands = {
            "python": ["python", []],
            "cpp": ["g++", ["-o"]],
            "java": ["javac", []],
            "javascript": ["node", []]
        }
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        # Language selector
        lang_layout = QHBoxLayout()
        self.lang_label = QLabel("Language:")
        self.lang_selector = QComboBox()
        self.lang_selector.addItems(["python", "cpp", "java", "javascript"])
        self.lang_selector.currentTextChanged.connect(self.change_language)
        lang_layout.addWidget(self.lang_label)
        lang_layout.addWidget(self.lang_selector)
        lang_layout.addStretch()
        layout.addLayout(lang_layout)
        
        # Create WebEngine View for Monaco Editor
        self.web_view = QWebEngineView()
        self.channel = QWebChannel(self)
        self.channel.registerObject("bridge", WebChannel(self))
        self.web_view.page().setWebChannel(self.channel)
        
        # Load Monaco Editor
        html_path = os.path.join(os.path.dirname(__file__), 'editor.html')
        self.web_view.setUrl(QUrl.fromLocalFile(html_path))
        
        layout.addWidget(self.web_view)
        
        # Test Case Input and Output
        test_case_layout = QHBoxLayout()
        
        # Input section
        input_layout = QVBoxLayout()
        self.input_label = QLabel("Input:")
        self.input_text = QPlainTextEdit()
        self.input_text.setMaximumHeight(100)
        input_layout.addWidget(self.input_label)
        input_layout.addWidget(self.input_text)
        
        # Output section
        output_layout = QVBoxLayout()
        self.output_label = QLabel("Output:")
        self.output_text = QPlainTextEdit()
        self.output_text.setMaximumHeight(100)
        self.output_text.setReadOnly(True)
        output_layout.addWidget(self.output_label)
        output_layout.addWidget(self.output_text)
        
        test_case_layout.addLayout(input_layout)
        test_case_layout.addLayout(output_layout)
        layout.addLayout(test_case_layout)
        
        # Run Button
        self.run_button = QPushButton("Run")
        self.run_button.clicked.connect(self.run_code)
        self.run_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 5px;
                border: none;
                border-radius: 3px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        layout.addWidget(self.run_button)
        
        self.setLayout(layout)

    def change_language(self, language):
        self.current_language = language
        self.web_view.page().runJavaScript(f"window.changeLanguage('{language}');")
    
    def run_code(self):
        self.web_view.page().runJavaScript(
            "editor.getValue();",
            self._handle_code_and_run
        )
    
    def _handle_code_and_run(self, code):
        try:
            input_data = self.input_text.toPlainText()
            output = self.run_code_with_language(code, input_data)
            self.output_text.setPlainText(output)
        except Exception as e:
            self.output_text.setPlainText(f"Error: {str(e)}")
    
    def run_code_with_language(self, code, input_data):
        temp_dir = tempfile.mkdtemp()
        try:
            if self.current_language == "python":
                return self.run_python(code, input_data, temp_dir)
            elif self.current_language == "cpp":
                return self.run_cpp(code, input_data, temp_dir)
            elif self.current_language == "java":
                return self.run_java(code, input_data, temp_dir)
            elif self.current_language == "javascript":
                return self.run_javascript(code, input_data, temp_dir)
        finally:
            shutil.rmtree(temp_dir)
    
    def run_python(self, code, input_data, temp_dir):
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
    
    def run_cpp(self, code, input_data, temp_dir):
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
    
    def run_java(self, code, input_data, temp_dir):
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
    
    def run_javascript(self, code, input_data, temp_dir):
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