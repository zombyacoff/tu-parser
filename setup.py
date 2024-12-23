from textwrap import dedent

from setuptools import setup


def get_requirements(file_name: str = "requirements.txt") -> list[str]:
    with open(file_name, "r") as file:
        return file.read().splitlines()


setup(
    name="tuparser",
    version="1.0.0",
    author="zombyacoff",
    author_email="zombyacoff@gmail.com",
    url="https://github.com/zombyacoff/tu-parser",
    description="A flexible module for building custom parsers for the Telegraph website",
    long_description=dedent("""\
        # Telegraph Universal Parser
        **Telegraph Universal Parser (tu-parser)** is a flexible module designed for creating custom parsers for the [Telegraph](https://telegra.ph) website.
        """),
    long_description_content_type="text/markdown",
    packages=["tuparser"],
    install_requires=get_requirements(),
    python_requires=">=3.12",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="parser scraper parser-api telegraph telegraph-api",
)
