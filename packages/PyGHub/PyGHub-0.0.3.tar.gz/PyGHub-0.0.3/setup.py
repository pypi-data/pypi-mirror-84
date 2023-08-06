import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyGHub",
    version="v0.0.3",
    author="FRostri",
    author_email="frostri.sho755@gmail.com",
    description="A github module for Python ",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FRostri/PyGHub",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Version Control",
        "Topic :: Software Development :: Version Control :: Git",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
