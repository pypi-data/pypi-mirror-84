import setuptools

PYTHON_VERSION="3.7"

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="automate-insurance-pricing", 
    version="0.0.1",
    author="Nassim Ezzakraoui",
    author_email="nassmim972@gmail.com",
    description="Bunch of functions for insurance pricing purposes",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/nassmim/automate-insurance-pricing",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='~=' + PYTHON_VERSION,
)