from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='pycell',
  version='1.2.4',
  description='A complex library containing multiple c-ell (cell) functions',
  long_description=open('README.txt').read() + '\n\n' + open('CHANGELOG.txt').read(),
  url='',  
  author='James Nortinski',
  author_email='james@j2k.pl',
  license='MIT', 
  classifiers=classifiers,
  keywords='pycell', 
  packages=find_packages(),
  install_requires=[''] 
)