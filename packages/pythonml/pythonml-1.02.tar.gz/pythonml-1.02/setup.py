from distutils.core import setup
setup(
  name = 'pythonml',         # How you named your package folder (MyLib)
  packages = ['pythonml'],   # Chose the same as "name"
  version = '1.02',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This hands-on Library is practical for AI and ML which facilitates viewing Dataset Integrity Reports, '
                'Viewing Accuracy Scores of Regressive and Classification algorithms, Instant and graphical '
                'comparison of ML Regressive and Classifier models of ML, Cleaning and Encoding of Dataset '
                'fitting custom ML models, visualizations of metrics, estimating goodness of fit etc. ',

  author = 'Aru Raghuvanshi',                   # Type in your name
  author_email = 'arusingh@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/hammeroflight/hammeroflight',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/user/reponame/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['data cleaning', 'accuracy scores', 'goodness of fit', 'dataset quality report', 'ML algo comparison'],
  install_requires=[            # I get to this in a second
          'numpy',
          'pandas', 'sklearn', 'XGboost', 'lightGBM', 'seaborn', 'matplotlib'
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.6',
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
  ],
)