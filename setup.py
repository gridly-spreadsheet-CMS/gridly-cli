from setuptools import setup

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

setup(
  name = 'gridly_cli',
  packages = ['gridly_cli'],
  version = '0.1.3',
  license='MIT',
  description = 'Gridly CLI',
  long_description=long_description,
  long_description_content_type='text/markdown',
  author = 'LD',
  author_email = 'cn@localizedirect.com',
  url = 'https://gridly.com',
  download_url = 'https://github.com/gridly-spreadsheet-CMS/gridly-cli/archive/refs/tags/0.1.3.tar.gz',
  keywords = ['GRIDLY', 'CLI', 'CMS', 'GRIDLY CLI'],
  install_requires=[
          'click',
          'requests',
          'questionary',
          'tabulate',
      ],
  entry_points='''
        [console_scripts]
        main=gridly_cli.main:gridly
    ''',
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      # Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)