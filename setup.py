# setup.py

from setuptools import setup, find_packages

setup(
    name='baseball-cli',
    version='0.1.0',
    entry_points = {
        'console_scripts': ['baseball-cli=src.cli:main'],
    },
    packages=find_packages(),
    author='Sumukh Venkatesh',
    description='A command-line interface tool for analyzing baseball stats and fantasy baseball teams.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    url='https://github.com/SilverCobra-prog/fantasy-CLI',
    classifiers=[
        'Programming Language :: Python :: 3',
        'Intended Audience :: End Users/Desktop',
        'Topic :: Games/Entertainment :: Sports',
        'License :: OSI Approved :: MIT License',
    ],
    python_requires='>=3.7',
)