import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="flopi",
    version="0.0.2",
    author="Jeff Webb",
    author_email="jeff.webb@codecraftsmen.org",
    description="Fine-grained logging and output Python interface",
    long_description=long_description,
    long_description_content_type="text/x-rst",
    url="https://github.com/codecraftingtools/flopi",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
