import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="csv-split",
    version=os.getenv('VERSION', default='0.0.0'),
    author="Bilal Fazlani",
    author_email="bilal.m.fazlani@gmail.com",
    description="A cli tool to split csv files",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bilal-fazlani/splitcsv",
    packages=setuptools.find_packages(),
    scripts=['csv_split/bin/csv-split'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
    keywords='csv file split bilal-fazlani'
)
