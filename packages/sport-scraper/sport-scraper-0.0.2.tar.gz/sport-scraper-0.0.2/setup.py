import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sport-scraper",
    version="0.0.2",
    author="Cristobal Mitchell",
    author_email="cristobalmitchell@gmail.com",
    description="Simple web scraper package for gathering sports data from ESPN.com",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/cristobalmitchell/sports-data-web-scraper",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)