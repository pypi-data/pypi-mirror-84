import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pandas_nested_dicts",
    version="0.0.1",
    author="Gianfrancesco Angelini",
    author_email="gian.angelini@hotmail.com",
    description="A small package to make easy to convert nested dicts to DataFrames and the vice versa",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/gianfa/pandas_dict_converter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6'
)