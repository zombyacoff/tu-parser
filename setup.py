from textwrap import dedent

from setuptools import find_packages, setup

import tuparser


def get_description() -> str:
    with open("README.md", "r") as file:
        return file.read()


def get_requirements(file_name: str = "requirements.txt") -> list[str]:
    with open(file_name, "r") as file:
        return file.read().splitlines()


setup(
    name="tuparser",
    version=tuparser.__version__,
    author=tuparser.__author__,
    author_email=tuparser.__email__,
    url=tuparser.__git_url__,
    license="GPL-3.0",
    description=
    "A module that facilitates the creation of Telegraph parsing scripts",
    # long_description=get_description(),
    long_description=dedent(f"""\
        # Telegraph Universal Parser
        A module that facilitates the creation of [Telegraph]({tuparser.TELEGRAPH_URL}) parsing scripts
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
