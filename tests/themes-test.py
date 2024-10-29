import unittest
from unittest.mock import patch, MagicMock
from PyQt5.QtWidgets import QApplication, QStyleFactory
from PyQt5.QtGui import QPalette, QColor
from PyQt5.QtCore import Qt
import sys
import os

# Add the parent directory of 'src' to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.themes import ThemeManager

class TestThemeManager(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        # Create a QApplication instance for the entire test suite
        if QApplication.instance() is None:
            cls.app = QApplication([])
        else:
            cls.app = QApplication.instance()

    def setUp(self):
        self.theme_manager = ThemeManager("Dark (Default)")

    def test_get_theme_names(self):
        theme_names = self.theme_manager.get_theme_names()
        expected_names = [
            "Dark (Default)", "Light", "Monokai", "Solarized", "Solarized Dark",
            "Dracula", "Nord", "Gruvbox", "One Dark"
        ]
        self.assertEqual(set(theme_names), set(expected_names))

    @patch('PyQt5.QtWidgets.QApplication.setPalette')
    def test_apply_dark_mode(self, mock_set_palette):
        self.theme_manager.apply_dark_mode()
        self.assertTrue(mock_set_palette.called)
        palette = mock_set_palette.call_args[0][0]
        self.assertEqual(palette.color(QPalette.Window), QColor(53, 53, 53))
        self.assertEqual(palette.color(QPalette.WindowText), Qt.white)
        self.assertEqual(palette.color(QPalette.Base), QColor(25, 25, 25))
        self.assertEqual(palette.color(QPalette.AlternateBase), QColor(53, 53, 53))
        self.assertEqual(palette.color(QPalette.ToolTipBase), Qt.white)
        self.assertEqual(palette.color(QPalette.ToolTipText), Qt.white)
        self.assertEqual(palette.color(QPalette.Text), Qt.white)
        self.assertEqual(palette.color(QPalette.Button), QColor(53, 53, 53))
        self.assertEqual(palette.color(QPalette.ButtonText), Qt.white)
        self.assertEqual(palette.color(QPalette.BrightText), Qt.red)
        self.assertEqual(palette.color(QPalette.Link), QColor(42, 130, 218))
        self.assertEqual(palette.color(QPalette.Highlight), QColor(42, 130, 218))
        self.assertEqual(palette.color(QPalette.HighlightedText), Qt.black)

    @patch('PyQt5.QtWidgets.QApplication.setPalette')
    def test_apply_light_mode(self, mock_set_palette):
        self.theme_manager.apply_light_mode()
        self.assertTrue(mock_set_palette.called)
        palette = mock_set_palette.call_args[0][0]
        self.assertEqual(palette.color(QPalette.Window), QColor(240, 240, 240))
        self.assertEqual(palette.color(QPalette.WindowText), Qt.black)
        self.assertEqual(palette.color(QPalette.Base), QColor(255, 255, 255))
        self.assertEqual(palette.color(QPalette.AlternateBase), QColor(240, 240, 240))
        self.assertEqual(palette.color(QPalette.ToolTipBase), Qt.white)
        self.assertEqual(palette.color(QPalette.ToolTipText), Qt.white)
        self.assertEqual(palette.color(QPalette.Text), Qt.black)
        self.assertEqual(palette.color(QPalette.Button), QColor(240, 240, 240))
        self.assertEqual(palette.color(QPalette.ButtonText), Qt.black)
        self.assertEqual(palette.color(QPalette.BrightText), Qt.red)
        self.assertEqual(palette.color(QPalette.Link), QColor(42, 130, 218))
        self.assertEqual(palette.color(QPalette.Highlight), QColor(42, 130, 218))
        self.assertEqual(palette.color(QPalette.HighlightedText), Qt.black)

    @patch('PyQt5.QtWidgets.QApplication.setPalette')
    def test_apply_monokai_mode(self, mock_set_palette):
        self.theme_manager.apply_monokai_mode()
        self.assertTrue(mock_set_palette.called)
        palette = mock_set_palette.call_args[0][0]
        self.assertEqual(palette.color(QPalette.Window), QColor(39, 40, 34))
        self.assertEqual(palette.color(QPalette.WindowText), QColor(248, 248, 242))
        self.assertEqual(palette.color(QPalette.Base), QColor(39, 40, 34))
        self.assertEqual(palette.color(QPalette.AlternateBase), QColor(39, 40, 34))
        self.assertEqual(palette.color(QPalette.ToolTipBase), QColor(248, 248, 242))
        self.assertEqual(palette.color(QPalette.ToolTipText), QColor(39, 40, 34))
        self.assertEqual(palette.color(QPalette.Text), QColor(248, 248, 242))
        self.assertEqual(palette.color(QPalette.Button), QColor(39, 40, 34))
        self.assertEqual(palette.color(QPalette.ButtonText), QColor(248, 248, 242))
        self.assertEqual(palette.color(QPalette.BrightText), QColor(255, 184, 108))
        self.assertEqual(palette.color(QPalette.Link), QColor(80, 120, 220))
        self.assertEqual(palette.color(QPalette.Highlight), QColor(80, 200, 120))
        self.assertEqual(palette.color(QPalette.HighlightedText), QColor(248, 248, 242))

    @patch('PyQt5.QtWidgets.QApplication.setPalette')
    def test_apply_solarized_mode(self, mock_set_palette):
        self.theme_manager.apply_solarized_mode()
        self.assertTrue(mock_set_palette.called)
        palette = mock_set_palette.call_args[0][0]
        self.assertEqual(palette.color(QPalette.Window), QColor(236, 239, 244))
        self.assertEqual(palette.color(QPalette.WindowText), QColor(42, 57, 66))
        self.assertEqual(palette.color(QPalette.Base), QColor(147, 161, 161))
        self.assertEqual(palette.color(QPalette.AlternateBase), QColor(236, 239, 244))
        self.assertEqual(palette.color(QPalette.ToolTipBase), QColor(42, 57, 66))
        self.assertEqual(palette.color(QPalette.ToolTipText), QColor(236, 239, 244))
        self.assertEqual(palette.color(QPalette.Text), QColor(42, 57, 66))
        self.assertEqual(palette.color(QPalette.Button), QColor(147, 161, 161))
        self.assertEqual(palette.color(QPalette.ButtonText), QColor(42, 57, 66))
        self.assertEqual(palette.color(QPalette.BrightText), QColor(197, 15, 31))
        self.assertEqual(palette.color(QPalette.Link), QColor(58, 151, 165))
        self.assertEqual(palette.color(QPalette.Highlight), QColor(35, 148, 109))
        self.assertEqual(palette.color(QPalette.HighlightedText), QColor(236, 239, 244))

    @patch('PyQt5.QtWidgets.QApplication.setPalette')
    def test_apply_solarized_dark_mode(self, mock_set_palette):
        self.theme_manager.apply_solarized_dark_mode()
        self.assertTrue(mock_set_palette.called)
        palette = mock_set_palette.call_args[0][0]
        self.assertEqual(palette.color(QPalette.Window), QColor(0, 43, 54))
        self.assertEqual(palette.color(QPalette.WindowText), QColor(131, 148, 150))
        self.assertEqual(palette.color(QPalette.Base), QColor(7, 54, 66))
        self.assertEqual(palette.color(QPalette.AlternateBase), QColor(0, 43, 54))
        self.assertEqual(palette.color(QPalette.ToolTipBase), QColor(131, 148, 150))
        self.assertEqual(palette.color(QPalette.ToolTipText), QColor(0, 43, 54))
        self.assertEqual(palette.color(QPalette.Text), QColor(131, 148, 150))
        self.assertEqual(palette.color(QPalette.Button), QColor(7, 54, 66))
        self.assertEqual(palette.color(QPalette.ButtonText), QColor(131, 148, 150))
        self.assertEqual(palette.color(QPalette.BrightText), QColor(220, 50, 47))
        self.assertEqual(palette.color(QPalette.Link), QColor(38, 139, 210))
        self.assertEqual(palette.color(QPalette.Highlight), QColor(135, 153, 0))
        self.assertEqual(palette.color(QPalette.HighlightedText), QColor(0, 43, 54))

    @patch('PyQt5.QtWidgets.QApplication.setPalette')
    def test_apply_dracula_mode(self, mock_set_palette):
        self.theme_manager.apply_dracula_mode()
        self.assertTrue(mock_set_palette.called)
        palette = mock_set_palette.call_args[0][0]
        self.assertEqual(palette.color(QPalette.Window), QColor(40, 42, 54))
        self.assertEqual(palette.color(QPalette.WindowText), QColor(248, 248, 242))
        self.assertEqual(palette.color(QPalette.Base), QColor(40, 42, 54))
        self.assertEqual(palette.color(QPalette.AlternateBase), QColor(44, 44, 44))
        self.assertEqual(palette.color(QPalette.ToolTipBase), QColor(248, 248, 242))
        self.assertEqual(palette.color(QPalette.ToolTipText), QColor(40, 42, 54))
        self.assertEqual(palette.color(QPalette.Text), QColor(248, 248, 242))
        self.assertEqual(palette.color(QPalette.Button), QColor(40, 42, 54))
        self.assertEqual(palette.color(QPalette.ButtonText), QColor(248, 248, 242))
        self.assertEqual(palette.color(QPalette.BrightText), QColor(255, 85, 85))
        self.assertEqual(palette.color(QPalette.Link), QColor(189, 147, 249))
        self.assertEqual(palette.color(QPalette.Highlight), QColor(255, 121, 198))
        self.assertEqual(palette.color(QPalette.HighlightedText), QColor(40, 42, 54))

    @patch('PyQt5.QtWidgets.QApplication.setPalette')
    def test_apply_nord_mode(self, mock_set_palette):
        self.theme_manager.apply_nord_mode()
        self.assertTrue(mock_set_palette.called)
        palette = mock_set_palette.call_args[0][0]
        self.assertEqual(palette.color(QPalette.Window), QColor(46, 52, 64))
        self.assertEqual(palette.color(QPalette.WindowText), QColor(216, 222, 233))
        self.assertEqual(palette.color(QPalette.Base), QColor(46, 52, 64))
        self.assertEqual(palette.color(QPalette.AlternateBase), QColor(59, 66, 76))
        self.assertEqual(palette.color(QPalette.ToolTipBase), QColor(216, 222, 233))
        self.assertEqual(palette.color(QPalette.ToolTipText), QColor(46, 52, 64))
        self.assertEqual(palette.color(QPalette.Text), QColor(216, 222, 233))
        self.assertEqual(palette.color(QPalette.Button), QColor(46, 52, 64))
        self.assertEqual(palette.color(QPalette.ButtonText), QColor(216, 222, 233))
        self.assertEqual(palette.color(QPalette.BrightText), QColor(207, 126, 112))
        self.assertEqual(palette.color(QPalette.Link), QColor(136, 192, 208))
        self.assertEqual(palette.color(QPalette.Highlight), QColor(163, 190, 140))
        self.assertEqual(palette.color(QPalette.HighlightedText), QColor(46, 52, 64))

    @patch('PyQt5.QtWidgets.QApplication.setPalette')
    def test_apply_gruvbox_mode(self, mock_set_palette):
        self.theme_manager.apply_gruvbox_mode()
        self.assertTrue(mock_set_palette.called)
        palette = mock_set_palette.call_args[0][0]
        self.assertEqual(palette.color(QPalette.Window), QColor(38, 35, 32))
        self.assertEqual(palette.color(QPalette.WindowText), QColor(253, 246, 227))
        self.assertEqual(palette.color(QPalette.Base), QColor(38, 35, 32))
        self.assertEqual(palette.color(QPalette.AlternateBase), QColor(50, 47, 45))
        self.assertEqual(palette.color(QPalette.ToolTipBase), QColor(253, 246, 227))
        self.assertEqual(palette.color(QPalette.ToolTipText), QColor(38, 35, 32))
        self.assertEqual(palette.color(QPalette.Text), QColor(253, 246, 227))
        self.assertEqual(palette.color(QPalette.Button), QColor(38, 35, 32))
        self.assertEqual(palette.color(QPalette.ButtonText), QColor(253, 246, 227))
        self.assertEqual(palette.color(QPalette.BrightText), QColor(235, 84, 104))
        self.assertEqual(palette.color(QPalette.Link), QColor(115, 145, 195))
        self.assertEqual(palette.color(QPalette.Highlight), QColor(150, 181, 106))
        self.assertEqual(palette.color(QPalette.HighlightedText), QColor(38, 35, 32))

    @patch('PyQt5.QtWidgets.QApplication.setPalette')
    def test_apply_one_dark_mode(self, mock_set_palette):
        self.theme_manager.apply_one_dark_mode()
        self.assertTrue(mock_set_palette.called)
        palette = mock_set_palette.call_args[0][0]
        self.assertEqual(palette.color(QPalette.Window), QColor(30, 30, 30))
        self.assertEqual(palette.color(QPalette.WindowText), QColor(248, 248, 242))
        self.assertEqual(palette.color(QPalette.Base), QColor(30, 30, 30))
        self.assertEqual(palette.color(QPalette.AlternateBase), QColor(36, 36, 36))
        self.assertEqual(palette.color(QPalette.ToolTipBase), QColor(248, 248, 242))
        self.assertEqual(palette.color(QPalette.ToolTipText), QColor(30, 30, 30))
        self.assertEqual(palette.color(QPalette.Text), QColor(248, 248, 242))
        self.assertEqual(palette.color(QPalette.Button), QColor(30, 30, 30))
        self.assertEqual(palette.color(QPalette.ButtonText), QColor(248, 248, 242))
        self.assertEqual(palette.color(QPalette.BrightText), QColor(255, 85, 85))
        self.assertEqual(palette.color(QPalette.Link), QColor(189, 147, 249))
        self.assertEqual(palette.color(QPalette.Highlight), QColor(255, 121, 198))
        self.assertEqual(palette.color(QPalette.HighlightedText), QColor(248, 248, 242))

if __name__ == '__main__':
    unittest.main()