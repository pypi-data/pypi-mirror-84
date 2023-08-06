from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='vedatbehpac',
  version='0.0.1',
  description='My first Python package',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='https://github.com/vedatapuk1/vedatbehpac',  
  author='Vedat Apuk',
  author_email='vedatapuk1@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='calculator', 
  package_dir={'': 'src'},
  packages=find_packages(where='src'),  # Required
  install_requires=[''] 
)