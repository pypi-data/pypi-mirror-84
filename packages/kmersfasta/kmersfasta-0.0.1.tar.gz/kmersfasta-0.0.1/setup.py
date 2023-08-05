# Import needed function from setuptools
from setuptools import setup

# Create proper setup to be used by pip
setup(name='kmersfasta',
      version='0.0.1',
      python_requires='>3.6.0',
      description='Display and count k-mers from the fasta file',
      author='Roshan Shrestha',
      packages=['kmersfasta'],
      install_requires=['biopython'])

