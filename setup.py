from setuptools import setup, find_packages

with open('Readme.md', 'r') as fh:
  long_description = fh.read()

setup(
  name='ranken',
  version='0.0.1',
  description='Finding Entanglement Rank',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author='plutoniumm',
  url='https://github.com/plutoniumm/ranken',
  license='MIT',
  package_dir={'': '.'},
  packages=find_packages(where='.'),
  python_requires='>=3.9',
  install_requires=[ 'numpy', 'scipy' ],
  extras_require={
    'dev': ['pytest', 'twine', 'wheel'],
  },
)
