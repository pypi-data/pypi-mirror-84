from distutils.core import setup
setup(
  name = 'Autosphere',         # How you named your package folder (MyLib)
  packages = ['Autosphere', 'Autosphere.Word', 'Autosphere.Desktop', 'Autosphere.Email', 'Autosphere.Excel', 'Autosphere.Outlook', 'Autosphere.Robocloud', 'Autosphere.core', 'Autosphere.includes'],   # Chose the same as "name"
  version = '0.5',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Autosphere skills to build RPA',   # Give a short description about your library
  author = 'Nauman Mahboob',                   # Type in your name
  author_email = 'nauman.mehboob@mercurialminds.com',      # Type in your E-Mail
  url = 'https://mercurialminds.com/',   # Provide either the link to your github or to your website
#   download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['RPA', 'Robot', 'Autosphere'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'robot',
          'selenium',
          'ConfigParser',
          'netsuitesdk',
          'notifiers',
          'fpdf',
          'pdfminer',
          'PyPDF2',
          'simple_salesforce',
          'graphviz',
          'tweepy',
          'boto3',
          'apiclient',
          'google',
          'clipboard',
          'pywinauto',
          'exchangelib',
          'pathlib',
          'openpyxl',
          'xlrd',
          'xlwt',
          'xlutils',
          'cryptography',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)