import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="API-StevenThomi",
    version="0.0.1",
    author="Steven Thomi",
    author_email="stevenkthomi@gmail.com",
    description="A temperature and luminosity sensor API package designed for Raspberry Pi",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/StevenThomi/eee3097s_project",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
