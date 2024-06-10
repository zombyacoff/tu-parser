from setuptools import setup


VERSION = "0.1.0"


def readme():
    with open("README.md", "r") as f:
        return f.read()


setup(
    name="tuparser",
    version=VERSION,
    
    author="zombyacoff",
    author_email="zombyacoff@gmail.com",
    
    url="https://github.com/zombyacoff/tu-parser",
    description="A module that facilitates the creation of Telegra.ph parsing scripts",
    long_description=readme(),
    long_description_content_type="text/markdown",
    
    packages=["tuparser"],
    install_requires=[
        "aiohttp>=3.9.5",
        "bs4>=0.0.2",
        "PyYaml>=6.0.1",
        "termcolor>=2.4.0",
    ],
    python_requires=">=3.12",
    
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.12",
    ],
    # keywords="telegra.ph parser scraper",
)
