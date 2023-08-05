# pylint: disable=missing-module-docstring
from distutils.core import setup
from setuptools import find_packages

setup(
    name='dotmgr',
    description='A small script that can help you maintain your dotfiles across several devices',
    keywords=['dotmgr', 'dotfile', 'management'],
    author='Sebastian Neuser',
    author_email='haggl@sineband.de',
    url='https://gitlab.com/haggl/dotmgr',
    license='GPLv3+',
    version='0.5.2',
    install_requires=['gitpython'],
    packages=find_packages(exclude=['tests']),
    entry_points={
        'console_scripts': [
            'dotmgr = dotmgr.cli:main',
        ]
    },
    extras_require={
        'dev': [
            'coverage',
            'nose',
            'setuptools',
            'wheel',
        ],
    },
)
