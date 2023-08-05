# Import needed function from setuptools
from setuptools import setup
with open("README.md", "r") as fh:
    long_description = fh.read()

# Create proper setup to be used by pip
setup(name='kmersfasta',
      version='0.0.3',
      python_requires='>3.6.0',
      long_description=long_description,
      long_description_content_type="text/markdown",
      description='Display and count k-mers from the fasta file',
      author='Roshan Shrestha',
      packages=['kmersfasta'],
      install_requires=['biopython'])

