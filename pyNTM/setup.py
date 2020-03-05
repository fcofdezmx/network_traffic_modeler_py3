import setuptools
from Cython.Build import cythonize

setuptools.setup(ext_modules=cythonize('*.pyx', annotate=True),
      package_data={'pyNTM':['./*']})
