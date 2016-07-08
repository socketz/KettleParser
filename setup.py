from codecs import open
from setuptools import setup, find_packages
from os import path

here = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(here, 'README.rst'), encoding='utf-8') as readme:
    long_description = readme.read()


setup(
    name='KettleParser',
    version='1.0.2',

    description='Library for parsing and analyzing Kettle XML files',
    long_description=long_description,

    # Get in touch with us!
    url='https://github.com/graphiq-data/KettleParser',
    author='Jeff Portwood - Graphiq Data Engineering',
    author_email='jportwood@graphiq.com',

    license='MIT',

    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
    ],

    keywords='kettle pdi pentaho',

    packages=find_packages(),
)