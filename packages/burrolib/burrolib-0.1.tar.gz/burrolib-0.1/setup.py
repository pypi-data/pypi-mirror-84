import setuptools
from setuptools import setup

with open('requirements.txt') as f:
    required = f.read().splitlines()

import numpy as np

setup(name='burrolib',
      version='0.1',
      description='burro - a supply chain simulator',
      author='Markus Semmler, Thomas Lautenschlaeger',
      author_email='dev@xploras.net',
      url="https://github.com/kosmitive/burro",
      install_requires=required,
      packages=setuptools.find_packages(),
      include_dirs=[np.get_include()],
      classifiers=[
            "Programming Language :: Python :: 3",
            "License :: OSI Approved :: MIT License",
            "Operating System :: OS Independent",
      ],
      python_requires='>=3.7',
      )
