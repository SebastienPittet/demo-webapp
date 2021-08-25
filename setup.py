# coding: utf-8
"""
A simple web application used in demo.
"""
from setuptools import find_packages, setup

with open('README.rst', 'r') as f:
    long_description = f.read()

setup(
   name='demo-webapp',
   version='0.0.4',
   author='Sebastien Pittet',
   author_email='sebastien@pittet.org',
   description='a simple web-app based on flask',
   long_description=long_description,
   url='https://github.com/SebastienPittet/demo-webapp',
   keywords='demo exoscale',
   packages=find_packages(),
   license='MIT',
   platforms='any',
   install_requires=[
       "Flask",
       "requests",
       "gunicorn"
   ],
   include_package_data=True,
   classifiers=[
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.6',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Intended Audience :: Other Audience'
    ]
)
