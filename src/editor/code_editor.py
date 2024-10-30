from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                           QPushButton, QPlainTextEdit, QComboBox, 
                           QScrollArea, QFrame, QSplitter)
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtCore import QUrl, Qt
from PyQt5.QtWebChannel import QWebChannel
import os
import tempfile
import shutil
from src.editor.run_code import (run_cpp, run_java, run_javascript, run_python)

class TestCaseWidget(QWidget):
    def __init__(self, input_data, expected_output, index, parent=None):
        super().__init__(parent)
        self.index = index
        self.initUI(input_data, expected_output)
        
    def initUI(self, input_data, expected_output):
        layout = QVBoxLayout()
        
        # Header with test case number
        header = QLabel(f"Test Case #{self.index + 1}")
        header.setStyleSheet("font-weight: bold; font-size: 14px;")
        layout.addWidget(header)
        
        # Input section
        input_label = QLabel("Input:")
        input_label.setStyleSheet("font-weight: bold;")
        self.input_text = QPlainTextEdit()
        self.input_text.setPlainText(input_data)
        self.input_text.setMaximumHeight(80)
        layout.addWidget(input_label)
        layout.addWidget(self.input_text)
        
        # Expected output section
        expected_label = QLabel("Expected Output:")
        expected_label.setStyleSheet("font-weight: bold;")
        self.expected_text = QPlainTextEdit()
        self.expected_text.setPlainText(expected_output)
        self.expected_text.setMaximumHeight(80)
        layout.addWidget(expected_label)
        layout.addWidget(self.expected_text)
        
        # Actual output section
        actual_label = QLabel("Actual Output:")
        actual_label.setStyleSheet("font-weight: bold;")
        self.actual_text = QPlainTextEdit()
        self.actual_text.setReadOnly(True)
        self.actual_text.setMaximumHeight(80)
        layout.addWidget(actual_label)
        layout.addWidget(self.actual_text)
        
        # Result label
        self.result_label = QLabel()
        self.result_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.result_label)
        
        # Add some spacing and a separator line
        line = QFrame()
        line.setFrameShape(QFrame.HLine)
        line.setFrameShadow(QFrame.Sunken)
        layout.addWidget(line)
        
        self.setLayout(layout)
    
    def update_result(self, actual_output, passed):
        self.actual_text.setPlainText(actual_output)
        if passed:
            self.result_label.setText("✓ PASSED")
            self.result_label.setStyleSheet("""
                QLabel {
                    color: #4CAF50;
                    font-weight: bold;
                    font-size: 14px;
                    padding: 5px;
                }
            """)
        else:
            self.result_label.setText("✗ FAILED")
            self.result_label.setStyleSheet("""
                QLabel {
                    color: #f44336;
                    font-weight: bold;
                    font-size: 14px;
                    padding: 5px;
                }
            """)

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
        self.test_cases = []
        self.test_case_widgets = []
        self.initUI()
        
    def initUI(self):
        layout = QHBoxLayout()
        
        # Left side: Editor section
        editor_widget = QWidget()
        editor_layout = QVBoxLayout()
        
        # Language selector
        lang_layout = QHBoxLayout()
        self.lang_label = QLabel("Language:")
        self.lang_selector = QComboBox()
        self.lang_selector.addItems(["python", "cpp", "java", "javascript"])
        self.lang_selector.currentTextChanged.connect(self.change_language)
        lang_layout.addWidget(self.lang_label)
        lang_layout.addWidget(self.lang_selector)
        lang_layout.addStretch()
        editor_layout.addLayout(lang_layout)
        
        # Monaco Editor
        self.web_view = QWebEngineView()
        self.channel = QWebChannel(self)
        self.channel.registerObject("bridge", QWebChannel(self))
        self.web_view.page().setWebChannel(self.channel)
        
        html_path = os.path.join(os.path.dirname(__file__), 'editor.html')
        self.web_view.setUrl(QUrl.fromLocalFile(html_path))
        editor_layout.addWidget(self.web_view)
        
        # Run Button
        self.run_button = QPushButton("Run All Test Cases")
        self.run_button.clicked.connect(self.run_code)
        self.run_button.setStyleSheet("""
            QPushButton {
                background-color: #4CAF50;
                color: white;
                padding: 8px;
                border: none;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
        """)
        editor_layout.addWidget(self.run_button)
        
        # Add Test Case Button
        self.add_test_case_button = QPushButton("Add Test Case")
        self.add_test_case_button.clicked.connect(self.add_test_case)
        editor_layout.addWidget(self.add_test_case_button)
        
        editor_widget.setLayout(editor_layout)
        
        # Right side: Test cases section
        test_cases_widget = QWidget()
        test_cases_layout = QVBoxLayout()
        
        # Header for test cases
        test_cases_header = QLabel("Test Cases")
        test_cases_header.setStyleSheet("""
            font-size: 16px;
            font-weight: bold;
            padding: 10px;
        """)
        test_cases_layout.addWidget(test_cases_header)
        
        # Scrollable area for test cases
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        
        # Container for test cases
        self.test_cases_container = QWidget()
        self.test_cases_container_layout = QVBoxLayout()
        self.test_cases_container_layout.addStretch()
        self.test_cases_container.setLayout(self.test_cases_container_layout)
        
        scroll_area.setWidget(self.test_cases_container)
        test_cases_layout.addWidget(scroll_area)
        
        test_cases_widget.setLayout(test_cases_layout)
        
        # Add splitter for resizable panels
        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(editor_widget)
        splitter.addWidget(test_cases_widget)
        splitter.setStretchFactor(0, 2)  # Editor gets 2/3 of the space
        splitter.setStretchFactor(1, 1)  # Test cases get 1/3 of the space
        
        layout.addWidget(splitter)
        self.setLayout(layout)

    def add_test_case(self):
        input_data = ""
        expected_output = ""
        self.test_cases.append((input_data, expected_output))
        
        # Create a new test case widget
        test_case_widget = TestCaseWidget(input_data, expected_output, len(self.test_cases) - 1)
        self.test_case_widgets.append(test_case_widget)
        self.test_cases_container_layout.insertWidget(
            self.test_cases_container_layout.count() - 1,  # Insert before stretch
            test_case_widget
        )
    
    def _handle_code_and_run(self, code):
        try:
            results = []
            for i, (input_data, expected_output) in enumerate(self.test_cases):
                output = self.run_code_with_language(code, input_data)
                passed = output.strip() == expected_output.strip()
                self.test_case_widgets[i].update_result(output, passed)
        except Exception as e:
            # Show error in all test cases
            for widget in self.test_case_widgets:
                widget.update_result(f"Error: {str(e)}", False)
    
    def change_language(self, language):
        self.current_language = language
        self.web_view.page().runJavaScript(f"window.changeLanguage('{language}');")
    
    def run_code(self):
        self.web_view.page().runJavaScript(
            "editor.getValue();",
            self._handle_code_and_run
        )
    
    def run_code_with_language(self, code, input_data):
        temp_dir = tempfile.mkdtemp()
        try:
            if self.current_language == "python":
                return run_python(code, input_data, temp_dir)
            elif self.current_language == "cpp":
                return run_cpp(code, input_data, temp_dir)
            elif self.current_language == "java":
                return run_java(code, input_data, temp_dir)
            elif self.current_language == "javascript":
                return run_javascript(code, input_data, temp_dir)
        finally:
            shutil.rmtree(temp_dir)
