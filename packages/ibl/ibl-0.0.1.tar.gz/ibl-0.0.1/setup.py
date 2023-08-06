from setuptools import setup, find_packages

classifiers = [
  'Development Status :: 5 - Production/Stable',
  'Intended Audience :: Developers',
  'Operating System :: Microsoft :: Windows :: Windows 10',
  'License :: OSI Approved :: MIT License',
  'Programming Language :: Python :: 3'
]

setup(
  name='ibl',
  version='0.0.1',
  description='Python api wrapper for infinity bot list',
  long_description="Docs Coming Soon",
  url='',
  author='Andromeda',
  author_email='bots@rjbot.xyz',
  license='MIT',
  classifiers=classifiers,
  keywords='infinity bot list',
  packages=find_packages(),
  install_requires=['aiohttp']
)
