# setup.py for abraxas
from setuptools import setup, find_packages

with open('README.md', 'r') as fh:
  long_description = fh.read()

setup(
  name='abraxas',
  version='0.0.1',
  description='A Quantum Circuit DSL',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author='plutoniumm',
  url="https://github.com/plutoniumm/abraxas",
  license='MIT',
  package_dir={'': 'src'},
  packages=find_packages(where='src'),
  python_requires='>=3.9',
  install_requires=['qiskit'],
  entry_points={
    'console_scripts': [
      'abraxas = abraxas.__main__:main'
    ]
  }
)