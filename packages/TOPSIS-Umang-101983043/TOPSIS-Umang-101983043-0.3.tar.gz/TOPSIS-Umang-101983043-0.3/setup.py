from distutils.core import setup
setup(
  name = 'TOPSIS-Umang-101983043',         # How you named your package folder (MyLib)
  packages = ['TOPSIS-Umang-101983043'],   # Chose the same as "name"
  version = '0.3',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'A simple python program to implement Multi Decision Criteria using TOPSIS',   # Give a short description about your library
  author = 'Umang Sharma',                   # Type in your name
  author_email = 'umangsharma.cs@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/umangSharmacs/TOPSIS-Umang-101983043',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/umangSharmacs/TOPSIS-Umang-101983043/archive/v_03.tar.gz',    # I explain this later on
  keywords = ['SIMPLE', 'CONCISE', 'TOPSIS', 'MULTI DECISION CRITERIA', 'DATASCIENCE'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'pandas',
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)