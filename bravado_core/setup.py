from distutils.core import setup
from Cython.Build import cythonize

setup(
    print('Cythonizing')
    ext_modules = cythonize("spec.pyx")
)
