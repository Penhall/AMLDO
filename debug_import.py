import importlib, sys, os
print(sys.version)
print('pkg dir', os.listdir('venv/Lib/site-packages/pydantic_core'))
try:
    import pydantic_core
    print('pydantic_core imported:', pydantic_core)
except Exception as e:
    print('Import pydantic_core failed:', repr(e))
try:
    m = importlib.import_module('pydantic_core._pydantic_core')
    print('submodule imported', m)
except Exception as e:
    print('Import submodule failed:', repr(e))
