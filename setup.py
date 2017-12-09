from distutils.core import setup

from panther import __version__

setup(name='PantherUI',
      version=__version__,
      description='A simple interface using Kivy for easy and quick game and graphical application development',
      author='tfff1OFFICIAL',
      author_email='tfff1s.modpacks@gmail.com',
      url='https://github.com/tfff1OFFICIAL/PantherUI',
      packages=['panther'],
      requires=[
          'Pillow',
          'docutils',
          'pygments',
          'pypiwin32',
          'kivy.deps.sdl2',
          'kivy.deps.glew',
          'kivy'
      ]
     )
