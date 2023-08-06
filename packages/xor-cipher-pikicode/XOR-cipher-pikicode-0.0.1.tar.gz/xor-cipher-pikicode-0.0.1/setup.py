import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="xor-cipher-pikicode", # Replace with your own username
    version="0.0.1",
    author="pikicode",
    author_email="info@pikicode.com",
    description="Simple XOR cipher",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Pikicode/XOR-cipher",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.2',
)
