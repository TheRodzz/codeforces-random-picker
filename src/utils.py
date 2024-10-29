import sys
import os
import shutil
import webbrowser
import json

def get_default_browser_name():
    """Get the name of the default system browser"""
    if sys.platform == 'darwin':  # macOS
        if os.path.exists('/Applications/Safari.app'):
            return 'Safari'
    elif sys.platform == 'win32':  # Windows
        return _get_windows_default_browser()
    else:  # Linux
        return _get_linux_default_browser()
    return 'System Browser'  # Fallback name if we can't detect the specific browser

def _get_windows_default_browser():
    import winreg
    try:
        with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                            r'SOFTWARE\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice') as key:
            browser_reg = winreg.QueryValueEx(key, 'ProgId')[0]
            for browser in ['Chrome', 'Firefox', 'Edge', 'Safari', 'Opera']:
                if browser in browser_reg:
                    return browser
    except Exception:
        pass
    return None

def _get_linux_default_browser():
    try:
        browser = os.popen('xdg-settings get default-web-browser').read().strip()
        for browser_name in ['firefox', 'chrome', 'chromium', 'safari', 'opera', 'edge']:
            if browser_name in browser.lower():
                return browser_name.capitalize()
    except Exception:
        pass
    return _detect_browsers_on_linux()

def _detect_browsers_on_linux():
    browsers_commands = {
        'firefox': 'Firefox',
        'google-chrome': 'Chrome',
        'chromium': 'Chromium',
        'opera': 'Opera',
        'microsoft-edge': 'Edge'
    }
    for cmd, name in browsers_commands.items():
        if shutil.which(cmd):
            return name
    return None

def get_available_browsers():
    """Get list of available browsers on the system"""
    browsers = {}
    
    # Add default browser first
    default_name = get_default_browser_name()
    browsers[f'{default_name} (Default)'] = ''

    # Try to detect common browsers
    for browser, cmd in _get_browser_commands().items():
        if shutil.which(cmd):
            try:
                webbrowser.get(cmd)
                browsers[browser] = cmd
            except webbrowser.Error:
                pass

    return browsers

def _get_browser_commands():
    browser_commands = {
        'Firefox': 'firefox',
        'Chrome': 'google-chrome' if sys.platform.startswith('linux') else 'chrome',
        'Chromium': 'chromium',
        'Safari': 'safari',
        'Edge': 'microsoft-edge' if sys.platform.startswith('linux') else 'edge',
        'Opera': 'opera'
    }
    return browser_commands

def load_preferences():
    """Load user preferences from a JSON file"""
    try:
        with open('preferences.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return {}

def save_preferences(preferences):
    """Save user preferences to a JSON file"""
    with open('preferences.json', 'w') as file:
        json.dump(preferences, file, indent=4)

def load_bookmarks():
    """Load bookmarks from a JSON file"""
    try:
        with open('bookmarks.json', 'r') as file:
            return json.load(file)
    except FileNotFoundError:
        return []

def save_bookmarks(bookmarks):
    """Save bookmarks to a JSON file"""
    with open('bookmarks.json', 'w') as file:
        json.dump(bookmarks, file, indent=4)