# -*- mode: python -*-

block_cipher = None



a = Analysis(['fcMain.py'],
             pathex=['./fc.controller', './fc.view', './fc.model', './fc.orm', './fc.misc', '/Users/wangjiangbin/gitlab/feeCalculate'],
             binaries=[],
             datas=[('./fc.misc/data-test.db','.')],
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
          a.binaries,
          a.zipfiles,
          a.datas,
          name='fcMain',
          debug=False,
          strip=False,
          upx=True,
          console=False , icon='fc.misc/zhnlk.ico')
app = BUNDLE(exe,
             name='fcMain.app',
             icon='./fc.misc/zhnlk.ico',
             bundle_identifier=None)
