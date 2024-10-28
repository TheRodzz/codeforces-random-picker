import sys
import os
import shutil
import webbrowser

def get_default_browser_name():
    """Get the name of the default system browser"""
    if sys.platform == 'darwin':  # macOS
        if os.path.exists('/Applications/Safari.app'):
            return 'Safari'
        
    elif sys.platform == 'win32':  # Windows
        import winreg
        
        try:
            with winreg.OpenKey(winreg.HKEY_CURRENT_USER, 
                                r'SOFTWARE\Microsoft\Windows\Shell\Associations\UrlAssociations\http\UserChoice') as key:
                browser_reg = winreg.QueryValueEx(key, 'ProgId')[0]
                
                if 'Chrome' in browser_reg:
                    return 'Chrome'
                elif 'Firefox' in browser_reg:
                    return 'Firefox'
                elif 'Edge' in browser_reg:
                    return 'Edge'
                elif 'Safari' in browser_reg:
                    return 'Safari'
                elif 'Opera' in browser_reg:
                    return 'Opera'
        except:
            pass
    
    else:  # Linux
        try:
            browser = os.popen('xdg-settings get default-web-browser').read().strip()
            if 'firefox' in browser.lower():
                return 'Firefox'
            elif 'chrome' in browser.lower():
                return 'Chrome'
            elif 'chromium' in browser.lower():
                return 'Chromium'
            elif 'safari' in browser.lower():
                return 'Safari'
            elif 'opera' in browser.lower():
                return 'Opera'
            elif 'edge' in browser.lower():
                return 'Edge'
        except:
            pass
            
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
                
    return 'System Browser'  # Fallback name if we can't detect the specific browser

def get_available_browsers():
    """Get list of available browsers on the system"""
    browsers = {}
    
    # Add default browser first
    default_name = get_default_browser_name()
    browsers[f'{default_name} (Default)'] = ''
    
    # Try to detect common browsers
    try:
        # Check for Firefox
        if shutil.which('firefox'):
            try:
                webbrowser.get('firefox')
                browsers['Firefox'] = 'firefox'
            except webbrowser.Error:
                pass

        # Check for Chrome
        chrome_cmd = 'google-chrome' if sys.platform.startswith('linux') else 'chrome'
        if shutil.which(chrome_cmd):
            try:
                webbrowser.get('chrome')
                browsers['Chrome'] = 'chrome'
            except webbrowser.Error:
                pass

        # Check for Chromium on Linux
        if sys.platform.startswith('linux') and shutil.which('chromium'):
            try:
                webbrowser.get('chromium')
                browsers['Chromium'] = 'chromium'
            except webbrowser.Error:
                pass

        # Check for Safari on macOS
        if sys.platform == 'darwin' and os.path.exists('/Applications/Safari.app'):
            try:
                webbrowser.get('safari')
                browsers['Safari'] = 'safari'
            except webbrowser.Error:
                pass

        # Check for Edge
        edge_cmd = 'microsoft-edge' if sys.platform.startswith('linux') else 'edge'
        if shutil.which(edge_cmd):
            try:
                webbrowser.get('edge')
                browsers['Edge'] = 'edge'
            except webbrowser.Error:
                pass

        # Check for Opera
        if shutil.which('opera'):
            try:
                webbrowser.get('opera')
                browsers['Opera'] = 'opera'
            except webbrowser.Error:
                pass

    except Exception as e:
        print(f"Error detecting browsers: {e}")
        
    return browsers