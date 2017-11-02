# -*- mode: python -*-

block_cipher = None


a = Analysis(['jg.py'],
             pathex=['/Users/liuyi/Documents/wwt/python/jgpy'],
             binaries=[],
             datas=[
             ('temp','temp'),
             ('support/lib/apksigner.jar','support/lib'),
             ('support/apksigner','support'),
             ('support/CheckAndroidV2Signature.jar','support'),
             ('support/walle-cli-all.jar','support'),
             ('support/zipalign','support')],
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
          name='jg',
          debug=False,
          strip=False,
          upx=True,
          console=False )
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='jg')
app = BUNDLE(coll,
             name='jg.app',
             icon=None,
             bundle_identifier=None)
