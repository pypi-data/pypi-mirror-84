import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='shirah-reader',
    version='0.1',
    long_description=README,
    url="https://github.com/hallicopter/shirah-reader",
    author="Hallicopter",
    author_email="advait.raykar@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=find_packages(),
    include_package_data=True,
    install_requires=["EbookLib", "beautifulsoup4", "syllables", "termcolor"],
    entry_points={
        "console_scripts": [
            "shirah = shirah:main",
        ]
    },
)