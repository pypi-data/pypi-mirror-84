#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from distutils.core import setup
from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'PixelP',         
  packages = ['PixelP'],  
  version = '0.4',     
  license='MIT',        
  description = 'Image augmeantation and preprocessing tool',   
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'Anirudh VM, Tanisha Bisarya, Aarsh Ghewde, Ekansh Trivedi, Yash Sawant' ,                 
  author_email = 'anirudh.vm63@nmims.edu.in',  
  url = 'https://github.com/AnirudhVm/PixelP',   
  download_url = 'https://github.com/AnirudhVm/PixelP/archive/0.4.tar.gz',   
  keywords = ['Image', 'Augment', 'Reshape','Color','Gray'],  
  install_requires=[          
          'validators',
          'beautifulsoup4',
      'numpy','pandas','opencv-python','keras'
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

