from setuptools import setup,find_packages
import os

setup(name='pubeasy',
      version='1',
      description='Boltzmann Transport Equation for Phonons',
      author='Giuseppe Romano',
      author_email='romanog@mit.edu',
      classifiers=['Programming Language :: Python :: 3.6'],
      license='GPLv2',\
      packages = ['pubeasy'],
      package_data = {'openbte':['fonts/*']},
      zip_safe=False)
