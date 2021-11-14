from setuptools import setup
import os, re

with open("README.md", "r") as fh:
    long_description = fh.read()


def get_version() -> str:
    """Get __version__ from __init__.py file."""
    version_file = os.path.join(os.path.dirname(__file__), "iabwrapper", "__init__.py")
    version_file_data = open(version_file, "rt", encoding="utf-8").read()
    version_regex = r"(?<=^__version__ = ['\"])[^'\"]+(?=['\"]$)"
    try:
        version = re.findall(version_regex, version_file_data, re.M)[0]
        return version
    except IndexError:
        raise ValueError(f"Unable to find version string in {version_file}.")


setup(
    name="IABwrapper",
    version=get_version(),
    packages=["iabwrapper"],
    package_data={"iabwrapper": ["*.py"],},
    # metadata to display on PyPI
    author="Shashi Ranjan",
    author_email="shashiranjankv@gmail.com",
    description="Wrapper around anjlab's Android In-app Billing Version 3 to be used in Kivy apps",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords="iab playstore billing android kivy-application kivy python",
    url="https://github.com/shashi278/android-iab-v3-kivy",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: Android",
    ],
    install_requires=["kivy"],
    python_requires=">=3.6",
)