from setuptools import setup
import sys

if sys.version_info < (3, ):
    raise ImportError('Python 2 is not supported. Consider upgrading to Python 3.')

readme = open('README.md').read()

setup(
    name = 'ataxx',
    version = '1.0',
    license = 'MIT',
    description = 'python-ataxx is written in Python 3 and supports basic features such as move generation, move validation, engine communication, and board printing.',
    long_description = readme,
    url = 'https://github.com/kz04px/python-ataxx',
    keywords = 'ataxx',
    packages = ['ataxx'],
    test_suite = 'test',
    extras_require = {
        'draw': 'Pillow'
    },
)
