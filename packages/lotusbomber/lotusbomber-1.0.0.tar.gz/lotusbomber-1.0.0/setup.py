from distutils.core import setup

setup(
  name = 'lotusbomber',         # How you named your package folder (MyLib)
  packages = ['lotusbomber'],   # Chose the same as "name"
  version = '1.0.0',      # Start with a small number and increase it with every change you make
  license='MPL-2.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Lotusbomber - Spammer for any messengers and social networks.',   # Give a short description about your library
  author = 'swiftlyfi',                   # Type in your name
  author_email = 'ban@pidor.men',      # Type in your E-Mail
  url = 'https://github.com/swiftlyfi/lotusbomber',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/swiftlyfi/lotusbomber/archive/1.0.0.tar.gz',    # I explain this later on
  keywords = ['SOME', 'MEANINGFULL', 'KEYWORDS'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          'PyAutoGUI',
          'pyfiglet',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',
    'Programming Language :: Python :: 3.7',
    "Operating System :: Microsoft :: Windows",
  ],
)
