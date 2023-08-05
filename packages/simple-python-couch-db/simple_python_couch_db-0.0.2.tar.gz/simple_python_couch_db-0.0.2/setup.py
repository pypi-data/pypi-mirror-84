import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="simple_python_couch_db",
    version="0.0.2",
    author="Oliver Schwamb",
    author_email="mail@oliverschwamb.de",
    description="Simple adapter to use CouchDB with Python.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bjoerndot",
    packages=setuptools.find_packages(),
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        'Programming Language :: Python :: 3.6',
        'Topic :: Database :: Front-Ends',
    ],
    python_requires='>=3.6',
    install_requires=['requests']
)