from setuptools import setup, find_packages

 
classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Operating System :: OS Independent',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]
 
setup(
  name='changer',
  version='3.0',
  description='Changer is - Arabic English Persian Hindi Chinese Malayalam Thai Bengali - Python library to convert numbers from-to.',
  long_description=open('README.md').read(),
  long_description_content_type="text/markdown",
  url='https://github.com/azwri/changer',  
  author='Azwri',
  author_email='aazwri@gmail.com',
  license='MIT', 
  classifiers=classifiers,
  keywords='Change Convert Arabic English Persian Hindi Chinese Malayalam Thai Bengali from to', 
  packages=find_packages(),
  install_requires=['']
)
