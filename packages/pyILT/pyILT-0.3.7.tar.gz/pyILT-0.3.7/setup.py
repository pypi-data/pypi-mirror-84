from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: POSIX :: Linux',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='pyILT',
  version='0.3.7',
  description='Extraction of data from ILThermo',
  long_description=[],
  url='',  
  author='Joao Ines - FCT-UNL',
  author_email='j.ines@fct.unl.pt',
  license='MIT', 
  classifiers=classifiers,
  keywords='ILThermo_DB', 
  packages=find_packages(),
  install_requires=[''] 
)
