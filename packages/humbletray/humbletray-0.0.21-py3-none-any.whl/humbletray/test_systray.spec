# -*- mode: python ; coding: utf-8 -*-


block_cipher = None


a = Analysis(['test_systray.py'],
             pathex=['F:\\Projects\\LAB\\humbletray\\humbletray'],
             binaries=[],
             datas=[('../templates', 'justpy/templates'), ('leaf.png', '.')],
             hiddenimports=['pystray._win32','schedule', 'uvicorn.lifespan.on','uvicorn.protocols.websockets.auto','uvicorn.protocols.http.auto','uvicorn.logging', 'uvicorn.loops.auto', 'uvicorn.protocols'],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher,
             noarchive=False)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          [],
          exclude_binaries=True,
          name='test_systray',
          debug=False,
          bootloader_ignore_signals=False,
          strip=False,
          upx=True,
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               upx_exclude=[],
               name='test_systray')
