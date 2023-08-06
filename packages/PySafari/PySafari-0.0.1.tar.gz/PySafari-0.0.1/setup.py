import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="PySafari", # Replace with your own username
    version="0.0.1",
    author="Vihaan Pundir",
    author_email="vihaan.pundir@ps517tccs.org",
    description="A small Safari like Python Web browser.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/pypa/PySafari",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)
