import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="tempmonitor-shamustch",
    version="0.0.1",
    author="Shamus Coughlin",
    author_email="shamustch@gmail.com",
    description="Temp Monitor",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/shamustch/TempMonitor",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)