__author__ = 'otger'

from setuptools import find_packages, setup

with open('HISTORY.md') as history_file:
    history = history_file.read()

setup(name="gfaaccesslib",
      version="1.1.0",
      description="A library to access GFA devices",
      author="Otger Ballester",
      author_email='otger@ifae.es',
      long_description_content_type="text/markdown",
      long_description=history,
      platforms=["any"],  # or more specific, e.g. "win32", "cygwin", "osx"
      license="BSD",
      packages=find_packages(),
      install_requires=[
            'numpy',
            'Pillow',
            'pytz',
      ],
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'License :: OSI Approved :: BSD License',
            'Programming Language :: Python :: 3'
      ],
)
