# setup.py

from setuptools import setup, find_packages

setup(
    name='fantasy-baseball-cli',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'requests>=2.25.1',
        'sqllite3>=3.50.1',
        'argparse>=3.2.1'
    ],
    entry_points={
        'console_scripts': [
            'fantasy-baseball=fantasy_baseball_cli.cli:main'
        ]
    },
    author='Sumukh Venkatesh',
    description='A command-line interface tool for analyzing baseball stats and fantasy baseball teams.',
    long_description=open('fantasy-baseball-cli/README.md').read(),
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