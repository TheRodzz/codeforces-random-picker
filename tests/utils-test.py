import unittest
from unittest.mock import patch, MagicMock, mock_open, call
import sys
import os
import json

# Add the parent directory of 'src' to the system path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))

from src.utils import (
    get_default_browser_name,
    _get_windows_default_browser,
    _get_linux_default_browser,
    _detect_browsers_on_linux,
    get_available_browsers,
    _get_browser_commands,
    load_preferences,
    save_preferences,
    load_bookmarks,
    save_bookmarks
)

class TestUtils(unittest.TestCase):

    @patch('sys.platform', 'darwin')
    @patch('os.path.exists', return_value=True)
    def test_get_default_browser_name_darwin(self, mock_exists):
        self.assertEqual(get_default_browser_name(), 'Safari')

    @patch('sys.platform', 'win32')
    @patch('src.utils._get_windows_default_browser', return_value='Chrome')
    def test_get_default_browser_name_win32(self, mock_get_windows_default_browser):
        self.assertEqual(get_default_browser_name(), 'Chrome')

    @patch('sys.platform', 'linux')
    @patch('src.utils._get_linux_default_browser', return_value='Firefox')
    def test_get_default_browser_name_linux(self, mock_get_linux_default_browser):
        self.assertEqual(get_default_browser_name(), 'Firefox')

    @unittest.skipUnless(sys.platform == "win32", "Windows-only test")
    @patch('winreg.OpenKey')
    @patch('winreg.QueryValueEx', return_value=('ChromeHTML',))
    def test_get_windows_default_browser(self, mock_query_value_ex, mock_open_key):
        self.assertEqual(_get_windows_default_browser(), 'Chrome')

    @patch('os.popen')
    def test_get_linux_default_browser(self, mock_popen):
        mock_popen.return_value.read.return_value = 'firefox.desktop\n'
        self.assertEqual(_get_linux_default_browser(), 'Firefox')

    @patch('shutil.which', side_effect=lambda x: x if x == 'firefox' else None)
    def test_detect_browsers_on_linux(self, mock_which):
        self.assertEqual(_detect_browsers_on_linux(), 'Firefox')

    @patch('src.utils.get_default_browser_name', return_value='Chrome')
    @patch('shutil.which', side_effect=lambda x: x if x in ['firefox', 'google-chrome'] else None)
    @patch('webbrowser.get', return_value=MagicMock())
    def test_get_available_browsers(self, mock_get_default_browser_name, mock_which, mock_webbrowser_get):
        browsers = get_available_browsers()
        self.assertIn('Chrome (Default)', browsers)
        self.assertIn('Firefox', browsers)
        self.assertIn('Chrome', browsers)
        self.assertEqual(browsers['Chrome (Default)'], '')
        self.assertEqual(browsers['Firefox'], 'firefox')
        self.assertEqual(browsers['Chrome'], 'google-chrome')


    def test_get_browser_commands(self):
        commands = _get_browser_commands()
        self.assertIn('Firefox', commands)
        self.assertIn('Chrome', commands)
        self.assertIn('Chromium', commands)
        self.assertIn('Safari', commands)
        self.assertIn('Edge', commands)
        self.assertIn('Opera', commands)

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps({'key': 'value'}))
    def test_load_preferences(self, mock_file):
        preferences = load_preferences()
        self.assertEqual(preferences, {'key': 'value'})

    # @patch('builtins.open', new_callable=mock_open)
    # def test_save_preferences(self, mock_file):
    #     preferences = {'key': 'value'}
    #     save_preferences(preferences)
    #     mock_file.assert_called_once_with('preferences.json', 'w')
    #     handle = mock_file()
    #     handle.write.assert_called_once_with(json.dumps(preferences, indent=4))

    @patch('builtins.open', new_callable=mock_open, read_data=json.dumps(['bookmark1', 'bookmark2']))
    def test_load_bookmarks(self, mock_file):
        bookmarks = load_bookmarks()
        self.assertEqual(bookmarks, ['bookmark1', 'bookmark2'])

    @patch('builtins.open', new_callable=mock_open)
    def test_save_bookmarks(self, mock_file):
        bookmarks = ['bookmark1', 'bookmark2']
        save_bookmarks(bookmarks)
        handle = mock_file()
        handle.write.assert_has_calls([
            call('[\n    "bookmark1"'), 
            call(',\n    "bookmark2"'), 
            call('\n'), 
            call(']')
        ])

if __name__ == '__main__':
    unittest.main()