import os
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

version = os.environ.get('PACKAGE_VERSION', '0.0.1.dev0')

setuptools.setup(
    name="quicksilver",
    version=version,
    author="Example Author",
    author_email="author@example.com",
    description="A small example package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/quicksilver",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
