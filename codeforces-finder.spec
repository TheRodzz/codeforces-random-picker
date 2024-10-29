import sys
from PyInstaller.building.build_main import Analysis, PYZ, EXE, COLLECT
from PyInstaller.utils.hooks import collect_all

# Collect all necessary data for PyQt5
datas = []
binaries = []
hiddenimports = []
tmp_ret = collect_all('PyQt5')
datas += tmp_ret[0]; binaries += tmp_ret[1]; hiddenimports += tmp_ret[2]

# Add the icon file
icon_path = 'icon.ico'

a = Analysis(
    ['main.py'],  
    pathex=[],
    binaries=binaries,
    datas=datas,
    hiddenimports=hiddenimports,
    hookspath=[],
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    noarchive=False
)

pyz = PYZ(a.pure, a.zipped_data)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='codeforces_finder',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    icon=icon_path  # Add this line to specify the icon
)

coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='codeforces_finder'
)