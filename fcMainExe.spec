# -*- mode: python -*-

block_cipher = None


a = Analysis(['fcMain.py'],
             pathex=['C:\\Users\\zhnlk\\AppData\\Local\\Programs\\Python\\Python35\\Lib\\site-packages\\PyQt5\\Qt\\bin\\', 
			 'C:\\Users\\zhnlk\\Documents\\gitcode\\feeCalculate\\fc.view\\', 
			 'C:\\Users\\zhnlk\\Documents\\gitcode\\feeCalculate\\fc.model\\', 
			 'C:\\Users\\zhnlk\\Documents\\gitcode\\feeCalculate\\fc.controller\\', 
			 'C:\\Users\\zhnlk\\Documents\\gitcode\\feeCalculate'],
             binaries=[],
             datas=[('C:\\Users\\zhnlk\\Documents\\gitcode\\feeCalculate\\data-test.db','.')],
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
          console=False , icon='C:\\Users\\zhnlk\\Documents\\gitcode\\feeCalculate\\zhnlk.ico')
