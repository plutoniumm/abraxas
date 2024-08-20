from setuptools import setup, find_packages

with open('Readme.md', 'r') as fh:
  long_description = fh.read()

setup(
  name='abrax',
  version='1.2.1',
  description='Cross platform circuit transpiler',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author='plutoniumm',
  url='https://github.com/plutoniumm/abraxas',
  license='MIT',
  package_dir={'': '.'},
  packages=find_packages(where='.'),
  python_requires='>=3.9',
  install_requires=[ 'numpy', 'qiskit'],
  extras_require={
    'dev': ['pytest', 'twine', 'wheel'],
  },
)
