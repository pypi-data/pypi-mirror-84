import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Base converter",
    version="0.1.0",
    author="Henri GASC",
    author_email="henri.gasc31@gmail.com",
    description="A code to convert from a numerical base to another",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Leoriem-code/Numerical-base-converter",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)