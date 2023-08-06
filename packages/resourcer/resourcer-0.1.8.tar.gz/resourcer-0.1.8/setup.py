import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="resourcer",
    version="0.1.8",
    author="Fiaz Sami",
    description="A simple wrapper around 'requests'",
    url="https://github.com/fiazsami/resourcer",
    packages=['resourcer',],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=[
        "requests",
    ],
    python_requires='>=3.6',
)
