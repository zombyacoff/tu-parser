from setuptools import find_packages, setup


def readme():
    with open("README.md", "r") as f:
        return f.read()


setup(
    name="tuparser",
    version="1.0.0",
    author="zombyacoff",
    author_email="zombyacoff@gmail.com",
    description="A module that facilitates the creation of Telegra.ph parsing scripts",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="home_link",
    packages=find_packages(),
    install_requires=[
        "aiohttp>=3.9.5",
        "bs4>=0.0.2",
        "PyYaml>=6.0.1",
        "termcolor>=2.4.0",
    ],
    classifiers=[
        "Programming Language :: Python :: 3.12",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    keywords="telegra.ph parser scraper",
    python_requires=">=3.12",
)
