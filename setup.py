from setuptools import setup

with open("README.md", 'r') as f:
    long_description = f.read()

setup(
   name='stm',
   version='0.2',
   description='A wrapper around Selenium webdriver that allows for easier management of tabs.',
   license="MIT",
   long_description=long_description,
   author='Jason Acheampong',
   author_email='jason.acheampong24@gmail.com',
   url="http://www.github.com/Mascerade/stm",
   packages=['stm'],
   install_requires=['selenium', 'urllib3']
)