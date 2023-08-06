import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="group-imputer", # Replace with your own username
    version="0.0.2",
    author="Eliott Kalfon",
    author_email="eliott.kalfon@gmail.com",
    description="Null imputing utility - work in progress",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/eliottkalfon/group-imputer",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)