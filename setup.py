# run as 'python setup.py build_ext --inplace'
from distutils.core import setup
from distutils.extension import Extension

try:
    from Cython.Build import cythonize
except ImportError:
    use_cython = False
else:
    use_cython = True


if use_cython:
    ext_modules = cythonize([
        Extension("pyNTM.circuit", ["pyNTM/circuit.py"]),
        Extension("pyNTM.demand", ["pyNTM/demand.py"]),
        Extension("pyNTM.interface", ["pyNTM/interface.py"]),
        Extension("pyNTM.model", ["pyNTM/model.py"]),
        Extension("pyNTM.exceptions", ["pyNTM/exceptions.py"]),
        Extension("pyNTM.node", ["pyNTM/node.py"]),
        Extension("pyNTM.rsvp", ["pyNTM/rsvp.py"]),
        Extension("pyNTM.srlg", ["pyNTM/srlg.py"]),
        Extension("pyNTM.utilities", ["pyNTM/utilities.py"]),
        Extension("pyNTM.parallel_link_model", ["pyNTM/parallel_link_model.py"]),
    ])
else:
    ext_modules = [
        Extension("pyNTM.circuit", ["pyNTM/circuit.c"]),
        Extension("pyNTM.demand", ["pyNTM/demand.c"]),
        Extension("pyNTM.interface", ["pyNTM/interface.c"]),
        Extension("pyNTM.model", ["pyNTM/model.c"]),
        Extension("pyNTM.exceptions", ["pyNTM/exceptions.c"]),
        Extension("pyNTM.node", ["pyNTM/node.c"]),
        Extension("pyNTM.rsvp", ["pyNTM/rsvp.c"]),
        Extension("pyNTM.srlg", ["pyNTM/srlg.c"]),
        Extension("pyNTM.utilities", ["pyNTM/utilities.c"]),
        Extension("pyNTM.parallel_link_model", ["pyNTM/parallel_link_model.c"]),
    ]

with open("requirements.txt", "r") as fs:
    reqs = [r for r in fs.read().splitlines() if (
        len(r) > 0 and not r.startswith("#"))]

version = '1.6'

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='pyNTM',
    version=version,
#    py_modules=['pyNTM'],
    ext_modules=ext_modules,
#    package_data={'pyNTM':['pyNTM/*.so']},
    install_requires=reqs,
#    include_package_data=True,
    description='Network traffic modeler API written in Python 3',
    long_description=long_description,
    long_description_content_type="text/markdown",
    author='Tim Fiola',
    author_email='timothy.fiola@gmail.com',
    url='https://github.com/tim-fiola/network_traffic_modeler_py3',
    download_url='https://github.com/tim-fiola/network_traffic_modeler_py3/tarball/%s' % version,
    keywords=['networking', 'layer3', 'failover', 'modeling', 'model', 'pyNTM'],
    classifiers=[],
)

