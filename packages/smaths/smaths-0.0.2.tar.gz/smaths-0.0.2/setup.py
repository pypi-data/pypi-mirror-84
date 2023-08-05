from setuptools import setup, find_packages
 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Education',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='smaths',
  version='0.0.2',
  description='Smath stands for SquareMATH. Algorithm written exclusively in Python and used to simplify square roots',
  long_description=open('readme.md').read() + '\n\n' + open('changelog.txt').read(),
  url='',  
  author='Mihai Focsa',
  author_email='saftuberraschung@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='simplificator', 
  packages=find_packages(),
  install_requires=[''] 
)
