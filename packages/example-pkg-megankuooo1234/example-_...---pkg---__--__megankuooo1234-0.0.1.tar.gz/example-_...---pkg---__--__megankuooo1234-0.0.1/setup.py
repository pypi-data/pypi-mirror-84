import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="example-_...---pkg---__--__megankuooo1234", # Replace with your own username
    version="0.0.1",
    author="Megan Kuo",
    author_email="megankuo@example.com",
    description="testing the name normalization of pep 503 with periods",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/sampleproject",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)

