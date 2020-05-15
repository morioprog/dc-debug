from setuptools import setup

setup(
    name="dc-debug",
    version="0.0.1",
    entry_points={
        "console_scripts": [
            "dc-debug = src.main:main"
        ]
    }
)
