# -*- mode: python ; coding: utf-8 -*-
import os
import paddlex

a = Analysis(
    ['main.py'],
    pathex=[],
    binaries=[],
    datas=[
        ('ppocr', 'ppocr'),
        (os.path.join(os.path.dirname(paddlex.__file__), '.version'), 'paddlex')
    ],
    hiddenimports=['paddlex'],
    hookspath=[],
    hooksconfig={},
    runtime_hooks=[],
    excludes=['skimage.io'],
    noarchive=False,
    optimize=0,
)
pyz = PYZ(a.pure)

exe = EXE(
    pyz,
    a.scripts,
    [],
    exclude_binaries=True,
    name='main',
    debug=False,
    bootloader_ignore_signals=False,
    strip=False,
    upx=True,
    console=True,
    disable_windowed_traceback=False,
    argv_emulation=False,
    target_arch=None,
    codesign_identity=None,
    entitlements_file=None,
)
coll = COLLECT(
    exe,
    a.binaries,
    a.datas,
    strip=False,
    upx=True,
    upx_exclude=[],
    name='main',
)
