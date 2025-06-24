# -*- mode: python ; coding: utf-8 -*-


a = Analysis(
    ['src/main.py'],
    pathex=['./src', './assets', './icons'],
    binaries=[],
    datas=[('src/GUI/styles.css', 'src/GUI'), ('./assets/*.png', 'assets')],
    hiddenimports=[],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=[],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    a.binaries,
    a.datas,
    [],
    name='Initiative Plus',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    upx_exclude=[],
    runtime_tmpdir=None,
    console=False,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
    icon='Initiative_Plus_Icon_Rounded.icn'
)
app = BUNDLE(
    exe,
    name='Initiative Plus.app',
    icon='Initiative_Plus_Icon_Rounded.icns',
    bundle_identifier=None,
)
