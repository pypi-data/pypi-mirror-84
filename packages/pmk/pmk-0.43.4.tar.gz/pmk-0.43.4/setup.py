import sys
from codecs import open
from os import path
from setuptools import setup, find_packages
from distutils.util import convert_path


# Import Version
main_ns = {}
ver_path = convert_path('pymake/_version.py')
with open(ver_path) as ver_file:
    exec(ver_file.read(), main_ns)


try:
    from Cython.Build import cythonize
    #from distutils.extension import Extension
except ImportError:
    CYTHON = False
else:
    CYTHON = 'bdist_wheel' not in sys.argv


# Requirements
_here = path.abspath(path.dirname(__file__))
with open(path.join(_here, 'requirements.txt'), encoding='utf-8') as f:
    all_reqs = f.read().split('\n')
install_requires = [x.strip() for x in all_reqs if not (x.strip().startswith(('#', '//')) or x.strip().endswith('?'))]
install_requires = list(filter(None, install_requires))

# Packages
packages = find_packages()
#packages += ['repo/ml'] +  ['repo/ml/'+p for p in find_packages('repo/ml/')]


setup(
    name='pmk',
    version=main_ns['__version__'],
    author='dtrckd',
    author_email='dtrckd@gmail.com',
    description='An experiment control system for reproducible research.',
    url='https://github.com/dtrckd/pymake',
    license='GPL',
    install_requires=install_requires,
    entry_points={
        'console_scripts': ['pmk=pymake.zymake:main'],
    },
    packages=packages,
    #package_dir={'ml' : 'repo/ml'},
    package_data={'pymake': ['pmk.cfg', 'template/*.template']},
    include_package_data=True,
    keywords=['pymake', 'learning', 'model'],
    classifiers=[
        'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Visualization',
        'Topic :: Scientific/Engineering :: Information Analysis',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Human Machine Interfaces',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Information Technology',
        'Intended Audience :: Science/Research',
        'Programming Language :: Python :: 3',
    ]

    ### Trying to cythonize the project (could help create a binary)
    #ext_modules=cythonize(
    #    "bhp/*.py", "bhp/**/*.py",
    #    #exclude=[
    #    #    'tatsu/__init__.py',
    #    #    'tatsu/codegen/__init__.py',
    #    #    'tatsu/test/*.py'
    #    #]
    #),

)
