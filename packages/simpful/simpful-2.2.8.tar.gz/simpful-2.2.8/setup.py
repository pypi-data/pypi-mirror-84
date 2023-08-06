from distutils.core import setup
setup(
  name = 'simpful',
  packages = ['simpful'], # this must be the same as the name above
  version = '2.2.8',
  description = 'A user-friendly Python library for fuzzy logic',
  author = 'Marco S. Nobile',
  author_email = 'm.s.nobile@tue.nl',
  url = 'https://github.com/aresio/simpful', # use the URL to the github repo
  keywords = ['fuzzy logic', 'sugeno', 'mamdani', 'reasoner', 'python', 'modeling'], # arbitrary keywords
  license='LICENSE.txt',
  install_requires=[
        "numpy >= 1.12.0",
        "scipy >= 1.0.0",
        "requests",
    ],
  classifiers = ['Programming Language :: Python :: 3.7'],
  long_description='simpful is a Python library for fuzzy logic reasoning, \
  designed to provide a simple and lightweight API, as close as possible \
  to natural language.',
)