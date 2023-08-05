#!/usr/bin/env python

from setuptools import setup

INSTALL_REQUIRES = [
    'numpy >= 1.14.3',
    'matplotlib >= 2.2.2',
    'mako ==1.0.12',
    'pandas >= 0.24.2',
    'scikit-learn >= 0.20.2',
    'pytest >= 4.6.2',
    'python-dateutil >= 2.7.3',
    'setuptools >= 39.1.0'
]

LONG_DESCRIPTION = """
The recent enforcement of data privacy protection regulations, such as GDPR,
has made data sharing more difficult. This tool intends to facilitate data
sharing from a customer by synthesizing a dataset based on the original dataset
for later machine learning.

There are two parts to this tool:

- Data synthesizer
  Synthesize a dataset based on the original dataset. It accepts CSV data as
  input, and output a synthesized dataset based on Differential Privacy. The
  algorithm in the data synthesizer reference to the paper (
  http://dimacs.rutgers.edu/~graham/pubs/papers/privbayes-tods.pdf).
- Data utility evaluation
  Evaluate the data utility for the synthesized dataset. The original dataset
  and the synthesized dataset as the input, one utility evaluation report will
  be generated with several indicators.
"""
URL = "https://github.com/SAP/data-synthesis-for-machine-learning"
PROJECT_URLS = {
    "Bug Tracker": URL + "/issues",
    "Documentation": URL,
    "Source Code": URL,
}


def main():
    setup(name='ds4ml',
          description='A python library for data synthesis and evaluation',
          long_description=LONG_DESCRIPTION,
          long_description_content_type='text/markdown',
          project_urls=PROJECT_URLS,
          url=URL,
          version='0.1.2',
          packages=['ds4ml', 'ds4ml.command'],
          package_data={
              '': ['template/*.html']
          },
          entry_points={
              'console_scripts': [
                  'data-synthesize = ds4ml.command.synthesize:main',
                  'data-evaluate = ds4ml.command.evaluate:main'
              ]
          },
          maintainer="Yan Zhao",
          maintainer_email="yan.zhao01@sap.com",
          install_requires=INSTALL_REQUIRES,
          platform='any')


if __name__ == '__main__':
    main()
