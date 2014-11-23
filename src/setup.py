from py2exe.build_exe import py2exe
from distutils.core import setup
#setup.py py2exe --includes sip
setup( windows=[{"script": "SP.pyw"}], options = {"py2exe": 
                                                  {"dll_excludes": ["MSVCP90.dll"],}
                                                  } )
