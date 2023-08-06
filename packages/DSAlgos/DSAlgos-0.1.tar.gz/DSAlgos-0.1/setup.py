import setuptools
from distutils.core import setup
setup(
  name = 'DSAlgos',         
  packages = ['DSAlgos'],   
  version = '0.1',     
  license='MIT',        
  description = 'Library for basic algorithms', 
  author = 'DSA', 
  author_email = 'niketbanetha@gmail.com',
  url = 'https://github.com/harshit-ladia/Algorithms',
  download_url = 'https://github.com/harshit-ladia/Algorithms/archive/v_01.tar.gz',  
  keywords = ['STACK', 'SORTING', 'SEARCHING', 'DSA'],
  install_requires=[        
          'validators',
          'beautifulsoup4',
      ],
  setup_requires=['wheel'],
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
