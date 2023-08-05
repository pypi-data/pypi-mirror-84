#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Oct 29 15:54:21 2020

@author: advait_t
"""
from distutils.core import setup
setup(
  name = 'pneumonia_pkg',         
  packages = ['pneumonia_pkg'],   
  version = '3.0',      
  license='MIT',        
  description = 'tool for detecting pneumonia',  
  author = 'Advait Thergaonkar, Jay Prajapati',                   
  author_email = 'advait.thergaonkar60@nmims.edu.in',     
  url = 'https://github.com/advait-t/pneumonia_package', 
  download_url = 'https://github.com/advait-t/pneumonia_package/archive/3.0.tar.gz',  
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