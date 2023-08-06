import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="origo-lambda-helpers",
    version="0.1.0",
    author="Oslo Origo",
    author_email="dataplattform@oslo.kommune.no",
    description="SDK for origo",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/oslokommune/origo-lambda-helpers-python",
    packages=setuptools.find_namespace_packages(
        include="origo.lambda_helpers.*", exclude=["tests*"]
    ),
    install_requires=[
        "structlog",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    zip_safe=False,
)

