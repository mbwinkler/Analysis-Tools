import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="TUMMET",
    version="0.0.1",
    author="Michael Winklerr",
    author_email="michael.b.winkler@tum.de",
    description="A packages to evaluate material test data",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mbwinkler/TUM-MET",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "TUMMET"},
    packages=setuptools.find_packages(where="TUMMET"),
    python_requires=">=3.9")
