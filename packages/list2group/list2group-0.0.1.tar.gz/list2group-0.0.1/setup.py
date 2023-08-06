
from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='list2group',    # This is the name of your PyPI-package.
    version='0.0.1',                          # Update the version number for new releases
    description="Generates a list with enumerated groups taking into account a change in consecutive values.",
    py_modules=["list2group"],
    package_dir={'':'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent"
    ],
    long_description = long_description,
    long_description_content_type="text/markdown",
    install_requires = [
        "numpy"
    ]
    
)
