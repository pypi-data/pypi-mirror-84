  
from setuptools import setup

from os import path

def get_long_description():
    with open(
        path.join(path.dirname(path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(name='durable_rules_tools',
      author='Tony Hirst',
      author_email='tony.hirst@open.ac.uk',
      install_requires=['durable_rules'],
      description='IPyhon magics for durable rules.',
      long_description=get_long_description(),
      long_description_content_type="text/markdown",
      license='MIT License',
      packages=['durable_rules_tools']
)