from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QTabWidget, QTextEdit, 
                           QPushButton, QHBoxLayout, QLabel, QPlainTextEdit,
                           QMessageBox, QComboBox)
from PyQt5.Qsci import QsciScintilla, QsciLexerPython, QsciLexerCPP
from PyQt5.QtGui import QColor, QFont
from PyQt5.QtCore import Qt
import subprocess
import tempfile
import os
import sys


class CodeEditor(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()
        
    def initUI(self):
        layout = QVBoxLayout()
        
        # Language selector
        lang_layout = QHBoxLayout()
        self.lang_label = QLabel("Language:")
        self.lang_selector = QComboBox()
        self.lang_selector.addItems(["C++", "Python"])
        self.lang_selector.currentTextChanged.connect(self.change_language)
        lang_layout.addWidget(self.lang_label)
        lang_layout.addWidget(self.lang_selector)
        lang_layout.addStretch()
        layout.addLayout(lang_layout)
        
        # Code Editor
        self.editor = QsciScintilla()
        self.setup_editor()
        layout.addWidget(self.editor)
        
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
        
    def setup_editor(self):
        # Font
        font = QFont("Consolas", 11)
        self.editor.setFont(font)
        
        # Margin for line numbers
        self.editor.setMarginType(0, QsciScintilla.NumberMargin)
        self.editor.setMarginWidth(0, "0000")
        self.editor.setMarginsForegroundColor(QColor("#ff888888"))
        
        # Indentation
        self.editor.setIndentationsUseTabs(False)
        self.editor.setTabWidth(4)
        self.editor.setAutoIndent(True)
        self.editor.setBackspaceUnindents(True)
        
        # Brace matching
        self.editor.setBraceMatching(QsciScintilla.SloppyBraceMatch)
        
        # Current line highlighting
        self.editor.setCaretLineVisible(True)
        self.editor.setCaretLineBackgroundColor(QColor("#1F1F1F"))
        self.editor.setCaretForegroundColor(QColor("white"))
        
        # Set initial lexer
        self.change_language("C++")
        
        # Edge mode shows a line at 80 characters
        self.editor.setEdgeMode(QsciScintilla.EdgeLine)
        self.editor.setEdgeColumn(80)
        self.editor.setEdgeColor(QColor("#FF333333"))
        
        # Default style
        self.editor.setMarginsBackgroundColor(QColor("#FF333333"))
        self.editor.setMarginsForegroundColor(QColor("#FF999999"))

    def change_language(self, language):
        if language == "C++":
            lexer = QsciLexerCPP()
        else:
            lexer = QsciLexerPython()
            
        # Set lexer colors
        lexer.setDefaultColor(QColor("#F8F8F2"))
        lexer.setDefaultPaper(QColor("#272822"))
        lexer.setDefaultFont(QFont("Consolas", 11))
        
        self.editor.setLexer(lexer)
        
    def run_code(self):
        try:
            code = self.editor.text()
            input_data = self.input_text.toPlainText()
            
            if self.lang_selector.currentText() == "C++":
                output = self.run_cpp_code(code, input_data)
            else:
                output = self.run_python_code(code, input_data)
                
            self.output_text.setPlainText(output)
            
        except Exception as e:
            QMessageBox.critical(self, "Error", str(e))
            
    def run_cpp_code(self, code, input_data):
        with tempfile.NamedTemporaryFile(suffix='.cpp', delete=False) as temp_file:
            temp_file.write(code.encode('utf-8'))
            temp_file_path = temp_file.name
            
        try:
            # Compile the code
            compile_command = ['g++', temp_file_path, '-o', temp_file_path + '.out']
            compile_process = subprocess.run(
                compile_command,
                capture_output=True,
                text=True
            )
            
            if compile_process.returncode != 0:
                return f"Compilation Error:\n{compile_process.stderr}"
                
            # Run the compiled code
            run_command = [temp_file_path + '.out']
            run_process = subprocess.run(
                run_command,
                input=input_data,
                capture_output=True,
                text=True,
                timeout=5  # 5 second timeout
            )
            
            if run_process.stderr:
                return f"Runtime Error:\n{run_process.stderr}"
                
            return run_process.stdout
            
        except subprocess.TimeoutExpired:
            return "Error: Program execution timed out (5 seconds)"
        except Exception as e:
            return f"Error: {str(e)}"
        finally:
            # Clean up
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)
            if os.path.exists(temp_file_path + '.out'):
                os.remove(temp_file_path + '.out')
                
    def run_python_code(self, code, input_data):
        with tempfile.NamedTemporaryFile(suffix='.py', delete=False) as temp_file:
            temp_file.write(code.encode('utf-8'))
            temp_file_path = temp_file.name
            
        try:
            run_process = subprocess.run(
                [sys.executable, temp_file_path],
                input=input_data,
                capture_output=True,
                text=True,
                timeout=5  # 5 second timeout
            )
            
            if run_process.stderr:
                return f"Error:\n{run_process.stderr}"
                
            return run_process.stdout
            
        except subprocess.TimeoutExpired:
            return "Error: Program execution timed out (5 seconds)"
        except Exception as e:
            return f"Error: {str(e)}"
        finally:
            if os.path.exists(temp_file_path):
                os.remove(temp_file_path)