from distutils.core import setup
from distutils.extension import Extension
from Cython.Distutils import build_ext

ext_modules = [
    Extension("common",  ["common.py"]),
    Extension("settings",  ["settings.py"]),
    Extension("import_all", ["import_all.py"]),
]
setup(
    name = 'fico21softlibs',
    cmdclass = {'build_ext': build_ext},
    ext_modules = ext_modules
)