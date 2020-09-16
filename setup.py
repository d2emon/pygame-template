from setuptools import setup, find_packages
from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
    name='d2game',
    version='1.0.0',
    description='Pygame template',
    long_description=long_description,

    url='https://github.com/d2emon/pygame-template',

    author='Dmitry Kutsenko',
    author_email='d2emonium@gmail.com',

    license='GPL 3.0',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'Programming Language :: Python :: 3.8',
    ],

    keywords='pygame template',

    packages=find_packages(),
    install_requires=['pygame'],
)
