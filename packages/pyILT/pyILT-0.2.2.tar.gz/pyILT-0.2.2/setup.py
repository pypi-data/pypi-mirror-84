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
  version='0.2.2',
  description='Extraction of data from ILThermo',
  long_description=open('/home/joao_ines/Documents/SLE/pyILThermo/README.txt').read() + '\n\n' + open('/home/joao_ines/Documents/SLE/pyILThermo/CHANGELOG.txt').read(),
  url='',  
  author='Joao Ines - FCT-UNL',
  author_email='j.ines@fct.unl.pt',
  license='MIT', 
  classifiers=classifiers,
  keywords='ILThermo_DB', 
  packages=find_packages(),
  install_requires=[''] 
)
