#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from distutils.core import setup
setup(
  name = 'PixelP',         
  packages = ['PixelP'],  
  version = '0.2',     
  license='MIT',        
  description = 'image augmeantation and preprocessing tool',   
  author = 'Anirudh VM, Tanisha Bisarya, Aarsh Ghewde, Ekansh Trivedi, Yash Sawant' ,                 
  author_email = 'anirudh.vm63@nmims.edu.in',  
  url = 'https://github.com/AnirudhVm/PixelP',   
  download_url = 'https://github.com/AnirudhVm/PixelP/archive/0.2.tar.gz',   
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

