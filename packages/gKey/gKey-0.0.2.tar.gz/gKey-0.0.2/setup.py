import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="gKey", # Replace with your own username
    version="0.0.2",
    author="gdavid7",
    description="Python library used to encrypt and decrypt strings in the simplest possible way, while also being incredibly secure.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gdavid7/gkey",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)