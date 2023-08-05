from distutils.core import setup
setup(
  name = 'juicysms',
  packages = ['juicysms'],  
  version = '0.1',
  license='MIT',
  description = 'A python wrapper for juicysms.com api',
  author = 'Jackson Green',
  author_email = 'jackson@inventive.dev',
  url = 'https://github.com/exploitdev/juicysms_python',
  download_url = 'https://github.com/exploitdev/juicysms_python',
  keywords = ['juicysms', 'API', 'SDK'],
  install_requires=[       
          'requests'
      ],
  classifiers=[
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3',     
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)