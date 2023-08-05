from setuptools import setup, find_packages
from glob import glob
import os.path

exec(open('predixy/_version.py').read())

setup(
    name='predixy',
    version=__version__,
    description='A command line program to predict NICS-XY scan results based on an additivity scheme.',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    author='Poranne group',
    author_email='renana.poranne@org.chem.ethz.ch',
    url='https://gitlab.com/porannegroup/predixy',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
    ],
    keywords='chemistry aromaticity PAH aroma',
    python_requires='>=3.7, <4',
    install_requires=['numpy>=1.19.2', 'scipy>=1.5.2', 'pandas>=1.1.2', 'tabulate>=0.8.7', 'matplotlib>=3.3.2', 'networkx>=2.5'],
    packages=['predixy',],
    package_dir={
        'predixy' : 'predixy',
    },
    package_data={
        'predixy' : ['config.ini', 'scan_data.csv'],
    },
    entry_points={
        'console_scripts': [
            'predixy=predixy:main',
        ],
    },
    license='GNU GPLv3',
)