# -*- mode: python ; coding: utf-8 -*-
# add

block_cipher = None

a = Analysis(
    ['app.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('templates', 'templates'),
        ('static', 'static'),
        ('fonts', 'fonts'),
        ('data', 'data'),
        ('scripts', 'scripts'),
    ],
    hiddenimports=['pypinyin', 'opencc', 'flask', 'reportlab.pdfbase.ttfonts', 'bs4'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    win_no_prefer_redirects=False,
    win_private_assemblies=False,
    cipher=block_cipher,
    noarchive=False,
)
pyz = PYZ(a.pure, a.zipped_data, cipher=block_cipher)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='wordwriter',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=True,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='static/logo_simple.icns',
)
coll = COLLECT(
    exe,
    a.binaries,
    a.zipfiles,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='wordwriter',
)
app = BUNDLE(
    coll,
    name='WordWriter.app',
    icon='static/logo_simple.icns',
    bundle_identifier='com.wordwriter.app',
    info_plist={
        'CFBundleShortVersionString': '1.0.0',
        'NSHumanReadableCopyright': '© 2025',
        'NSHighResolutionCapable': 'True',
    },
)