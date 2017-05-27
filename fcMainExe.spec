# -*- mode: python -*-

block_cipher = None


a = Analysis(['fcMain.py'],
             pathex=['C:\\Users\\zhnlk\\AppData\\Local\\Programs\\Python\\Python35\\Lib\\site-packages\\PyQt5\\Qt\\bin\\',
			 'C:\\Users\\zhnlk\\Documents\\gitcode\\feeCalculate\\view\\',
			 'C:\\Users\\zhnlk\\Documents\\gitcode\\feeCalculate\\models\\',
			 'C:\\Users\\zhnlk\\Documents\\gitcode\\feeCalculate\\controller\\',
			 'C:\\Users\\zhnlk\\Documents\\gitcode\\feeCalculate\\utils\\',
			 'C:\\Users\\zhnlk\\Documents\\gitcode\\feeCalculate\\services\\',
			 'C:\\Users\\zhnlk\\Documents\\gitcode\\feeCalculate'],
             binaries=[],
             datas=[('./fee.config','.')],
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
          console=True )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='fcMain')
