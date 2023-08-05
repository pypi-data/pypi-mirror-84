"""Set up hiapi
"""

from setuptools import setup

setup(
    name='pyhiapi',
    version='0.1.5',
    author='Ryan Jung',
    author_email='ryanjjung@gmail.com',
    packages=['hiapi'],
    url='https://github.com/ryanjjung/pyhiapi',
    license='LICENCE',
    description='PyHiAPI - Simple test API',
    long_description=open('README.md').read(),
    install_requires=[
        'flask'
    ],
    entry_points={
        'console_scripts': [
            'hiapi = hiapi.hi:main'
        ]
    }
)
