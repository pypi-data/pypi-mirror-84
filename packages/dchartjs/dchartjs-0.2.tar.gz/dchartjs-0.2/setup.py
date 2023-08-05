from setuptools import setup, find_packages

from os import path
this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    README = f.read()

setup(
    name="dchartjs",
    long_description=README,
    long_description_content_type='text/markdown',
    version="0.2",
    author="Shiva Gangula",
    author_email="shiva.gangula@outlook.com",
    description="Frontend Charts for django",
    license="MIT",
    keywords="dchartjs",
    install_requires=[],
    url="https://github.com/KrezyKiller/dchartjs",
    packages=find_packages(),
)