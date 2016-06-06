import sys
from os.path import join, dirname
from setuptools import setup
from setuptools.command.test import test

VERSION = '0.0.4'


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


class PyTest(test):
    def finalize_options(self):
        test.finalize_options(self)
        self.test_args = ['tests_merkapi']
        self.test_suite = True

    def run_tests(self):
        # import here, cause outside the eggs aren't loaded
        import pytest
        errno = pytest.main(self.test_args)
        sys.exit(errno)


setup(
    name='merk-api',
    version=VERSION,
    description='Merk API Python client',
    long_description=long_description,
    author='Vitek Pliska',
    author_email='vitek@creatiweb.cz',
    license='BSD',
    url='https://api.merk.cz/docs/',

    packages=('merkapi', 'tests_merkapi'),
    include_package_data=True,

    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: BSD License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Topic :: Utilities",
    ],

    setup_requires=setup_requires,
    install_requires=install_requires,
    tests_require=tests_require,

    cmdclass={'test': PyTest},
)
