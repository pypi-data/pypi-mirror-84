import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="rotate-logger",
    version="1.0.0",
    author="Reza Andriyunanto",
    author_email="andriyunantoreza@gmail.com",
    description="Package for rotating logger",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/rezandry/rotating-logger-python",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)