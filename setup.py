from setuptools import setup, find_packages

with open('Readme.md', 'r') as fh:
  long_description = fh.read()

setup(
  name='abrax',
  version='0.2.0',
  description='A Quantum Circuit DSL',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author='plutoniumm',
  url="https://github.com/plutoniumm/abrax",
  license='MIT',
  package_dir={'': 'src'},
  packages=find_packages(where='src'),
  python_requires='>=3.9',
  install_requires=[],
  extras_require={
    'dev': ['pytest', 'twine', 'wheel'],
  },
)