from setuptools import setup

with open("README.md", "r") as file: description = file.read()
    
setup(
    name="attribmanager",
    version="1.0",    
    description="A simple pythonic module to lock (make read-only) and hide class attributes",
    long_description=description,
    long_description_content_type="text/markdown",
    url="https://github.com/judev1/attribmanager",
    author="Jude BC",
    author_email="jude.version1.0@gmail.com",
    license="BSD 2-clause",
    packages=["attribmanager"],

    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",  
        "Operating System :: Microsoft",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
    ],
)
