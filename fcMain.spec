# -*- mode: python -*-

block_cipher = None


a = Analysis(['fcMain.py'],
             pathex=['./fc.controller', './fc.view', './fc.model', '/Users/wangjiangbin/gitlab/feeCalculate'],
             binaries=[],
             datas=[('./data-test.db','.')],
             hiddenimports=[],
             hookspath=[],
             runtime_hooks=[],
             excludes=[],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='fcMain',
          debug=False,
          strip=False,
          upx=True,
          console=False, 
          icon='./zhnlk.ico' )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='fcMain')
