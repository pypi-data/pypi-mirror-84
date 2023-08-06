import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple-augment",
    version="1.0",
    author="Zach Hafen",
    author_email="zachary.h.hafen@gmail.com",
    description="A collection of small but useful Python tools.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zhafen/augment",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    py_modules=[ 'augment', ],
)
