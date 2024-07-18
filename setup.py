from textwrap import dedent

from setuptools import find_packages, setup

import tuparser


def get_requirements(file_name: str = "requirements.txt") -> list[str]:
    with open(file_name, "r") as file:
        return file.read().splitlines()


setup(
    name="tuparser",
    version=tuparser.__version__,
    author=tuparser.__author__,
    author_email=tuparser.__email__,
    url=tuparser.__git_url__,
    description="A flexible module for building custom parsers for the Telegraph website",
    long_description=dedent(f"""\
        # Telegraph Universal Parser
        **Telegraph Universal Parser (tu-parser)** is a flexible module designed for creating custom parsers for the [Telegraph]({tuparser.TELEGRAPH_URL}) website.
        """),
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=get_requirements(),
    python_requires=">=3.12",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3.12",
    ],
    keywords="parser scraper parser-api telegraph telegraph-api",
)
