from setuptools import setup, find_packages
setup(
  name = 'squeemtools',
  packages = ['squeemtools'],
  version = '1.0.4',
  license='MIT',
  description = 'Packages for running some lightning graphing code',
  author = 'Ben van Oostendorp',
  author_email = 'ben.vano@digipen.edu',
  url = 'https://github.com/Squeemos/SqueemTools',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/Squeemos/SqueemTools/archive/SqueemTools_1.0.4.tar.gz',    # I explain this later on
  keywords = ['GRAPHING', 'FUZZY C MEANS','GLM'],
  install_requires=[
          'matplotlib',
          'numpy',
          'pandas',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',
    'Intended Audience :: Developers',
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',
    'Programming Language :: Python :: 3.8',
  ],
)