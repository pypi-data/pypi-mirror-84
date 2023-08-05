

from setuptools import find_packages, setup
from imghst.__version__ import Version


setup(
    name="imghst",
    version=str(Version()),
    author="Mustafa Mohamed",
    author_email="git@ms7m.me",
    description="A simple and fast image hoster for applications like ShareX.",
    long_description="A simple and fast image hoster for applications like ShareX.",
    long_description_content_type="text/markdown",
    url="https://github.com/ms7m/imghst",
    python_requires=">=3.6.0",
    packages=find_packages(
        exclude=["testing", "*.testing", "*.testing.*", "testing.*"]
    ),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points={
        "console_scripts": [
            "imghst = imghst.entry:cli_app"
        ]
    },
    include_package_data=True,
    install_requires=open("./requirements.txt", 'r').readlines())
