from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='pycellsewew',
  version='1.2.8',
  description='A simple and flexible Python3 library for Cell',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='James Nordinski',
  author_email='james@onet.pl',
  license='MIT', 
  classifiers=classifiers,
  keywords='cell', 
  packages=find_packages(),
  install_requires=[''] 
)
