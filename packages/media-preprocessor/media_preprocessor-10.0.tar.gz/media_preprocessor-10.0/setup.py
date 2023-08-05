from setuptools import setup, Extension
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'media_preprocessor',         
  packages = ['media_preprocessor'],   
  long_description=long_description,
  long_description_content_type='text/markdown',
  version = '10.0',      
  license='MIT',        
  description = 'tool for preprocessing media',  
  author = 'Harsh Mahajan, Akash Patil, Pranit Shriyan, Jayesh Singh, Shankh Suri, Tazeem Khan',                   
  author_email = 'harsh.mahajan28@nmims.edu.in',     
  url = 'https://github.com/harshh-mahajan/media_preprocessor', 
  download_url = 'https://github.com/harshh-mahajan/media_preprocessor/archive/10.0.tar.gz',  
  keywords = ['image', 'preprocessing', 'reshape','resize','background'],  
  install_requires=[            
          'validators',
          'beautifulsoup4'
          ,'numpy','pandas','opencv-python','matplotlib'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',     
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License', 
    'Programming Language :: Python :: 3',    
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)
