#!/usr/bin/env python

from setuptools import setup, find_packages


setup(
    name='gpam-pre-processing-ner',
    version='0.0.2',
    description='GPAM ner pre-processing',
    author='GPAM',
    author_email='gpam@gmail.com',
    url='https://gitlab.com/gpam/services/pre-processing-ner',
    packages=find_packages(),
    install_requires=[
      'nltk>=3.4.5',
      'numpy>=1.18.3',
      'requests>=2.23.0',
      'scikit-learn>=0.22.2.post1',
      'spacy>=2.2.4',
      'tensorflow==1.15.2',
      'tqdm>=4.45.0',
      'cached_property==1.5.2',
    ],
)
