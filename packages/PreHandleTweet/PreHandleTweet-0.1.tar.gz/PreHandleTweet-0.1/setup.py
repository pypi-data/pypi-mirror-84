from distutils.core import setup
setup(
  name = 'PreHandleTweet',         # How you named your package folder (MyLib)
  packages = ['PreHandleTweet'],   # Chose the same as "name"
  version = '0.1',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'This Helps in handling and cleaning the tweet without hassles.',   # Give a short description about your library
  author = 'Eshan Chatty',                   # Type in your name
  author_email = 'eshunew@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/chattyy/PreHandleTweet',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/chattyy/PreHandleTweet/archive/v_01.tar.gz',    # I explain this later on
  keywords = ['Tweet', 'PreProcess', 'NLTK'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          're',
          'string','numpy','nltk.corpus','nltk.stem','nltk.tokenize'
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
