#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from distutils.core import setup
setup(
  name = 'FinAvn2',
  packages = ['FinAvn2'],
  version = '0.7',
  license='MIT',
  description = 'Performing Financial Time series forecasting using Machine Learning',
  author = 'Avneesh Dubey',
  author_email = 'avneesh.d01@gmail.com',
  url = 'https://github.com/avneeshdubey99/FinAvn',
  download_url = 'https://github.com/avneeshdubey99/FinAvn.git',
  keywords = ['Machine Learning', 'Pandas', 'Numpy', 'Analysis', 'Regression', 'Classification', 'Dimensionality', 'Classifiers'],
  install_requires=[
          'numpy',
          'sklearn',
          'pandas'
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
    