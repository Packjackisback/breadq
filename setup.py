from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="breadq",
    version="0.1.0",
    author="Jack",
    author_email="packjackisback@gmail.com",
    description="Multiplayer client for QBReader",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/packjackisback/breadq",
    packages=find_packages(),
    install_requires=[
        "websockets>=11.0",
    ],
    python_requires=">=3.9",
)

