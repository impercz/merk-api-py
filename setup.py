from os.path import join, dirname
from setuptools import setup

VERSION = '0.0.3'


def parse_reqs(f='requirements.pip'):
    ret = []
    with open(join(dirname(__file__), f)) as fp:
        for l in fp.readlines():
            l = l.strip()
            if l and not l.startswith('#'):
                ret.append(l)
    return ret

setup_requires = ['setuptools']
install_requires, tests_require = parse_reqs(), parse_reqs('requirements-test.pip')

with open('README.md') as readmefile:
    long_description = readmefile.read()

setup(
    name='merk-api',
    version=VERSION,
    description='Merk API Python client',
    long_description=long_description,
    author='Vitek Pliska',
    author_email='vitek@creatiweb.cz',
    license='BSD',
    url='https://api.merk.cz/docs/',

    packages=('merkapi',),
    include_package_data=True,

    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.5",
        "Topic :: Utilities",
    ],

    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=tests_require,
)
