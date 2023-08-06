import os
import setuptools

lib_folder = os.path.dirname(os.path.realpath(__file__))
requirements_path = lib_folder + '/requirements.txt'
install_requires = []
if os.path.isfile(requirements_path):
    with open(requirements_path) as f:
        install_requires = f.read().splitlines()

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PyGHub",
    install_requires=install_requires,
    version="v0.0.4",
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
