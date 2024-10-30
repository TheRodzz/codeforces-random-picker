from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QPlainTextEdit, QFrame)

from PyQt5.QtCore import Qt


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