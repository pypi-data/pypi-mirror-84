import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Kelivery", 
    version="0.0.1",
    author="Zayne",
    author_email="saynemarsh9@gmail.com",
    description="Make your own custom installer with Kelivery.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/porplax/Kelivery-Module",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)