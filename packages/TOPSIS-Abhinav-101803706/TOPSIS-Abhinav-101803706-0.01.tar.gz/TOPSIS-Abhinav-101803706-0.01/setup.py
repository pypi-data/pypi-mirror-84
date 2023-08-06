from distutils.core import setup

# with open("README.md", "r") as fh:
#     long_description = fh.read()

setup(
  name = 'TOPSIS-Abhinav-101803706',        
  version = '0.01',    
  license='MIT',      
  description = 'A package for python implemetation of TOPSIS method for multiple criteria decision making', 
  # long_description="long_description",
  # long_description_content_type="text/markdown",
  author = 'Abhinav Goyal',                  
  author_email = 'zabhi1292@gmail.com',     
  url = 'https://github.com/zabhitak/TOPSIS-Abhinav-101803706',  
  download_url = 'https://github.com/zabhitak/TOPSIS-Abhinav-101803706/archive/0.12.tar.gz',    
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   
  install_requires=[          
          'numpy',
          'pandas',
          'scipy',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      
    'Intended Audience :: Developers',     
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   
    'Programming Language :: Python :: 3',     
    'Programming Language :: Python :: 3.7',
  ],
)

