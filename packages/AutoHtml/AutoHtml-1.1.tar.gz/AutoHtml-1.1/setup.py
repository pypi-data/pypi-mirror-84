from distutils.core import setup
setup(
  name = 'AutoHtml',         # How you named your package folder (MyLib)
  packages = ['AutoHtml'],   # Chose the same as "name"
  version = '1.1',      # Start with a small number and increase it with every change you make
  license='gpl-3.0',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Create Html using Object Oriented Programming technique',   # Give a short description about your library
  author = 'Noli Valdez III',                   # Type in your name
  author_email = 'nolivaldeziii@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/nvaldeziii/AutoHtml',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/nvaldeziii/AutoHtml/archive/1.1.tar.gz',    # I explain this later on
  keywords = ['html', 'oop'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
            'htmlmin'
      ],
  classifiers=[
    'Development Status :: 4 - Beta',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3',      #Specify which python versions that you want to support
    'Programming Language :: Python :: 3.4',
    'Programming Language :: Python :: 3.5',
    'Programming Language :: Python :: 3.6',
  ],
)