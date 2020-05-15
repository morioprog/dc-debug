from setuptools import find_packages, setup

setup(
    name="dc-debug",
    version="0.0.1",
    packages=find_packages(exclude=('test')),
    entry_points={
        "console_scripts": [
            "dc-debug = src.main:main"
        ]
    }
)
