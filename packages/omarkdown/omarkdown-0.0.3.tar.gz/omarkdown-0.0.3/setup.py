import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="omarkdown",
    version="0.0.3",
    author="MANITEJA",
    packages=['omnidoc'],
    author_email="teja3536mani@gmail.com",
    description="Markdown conversion to html using lark",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/omnidoc/omnidoc",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
