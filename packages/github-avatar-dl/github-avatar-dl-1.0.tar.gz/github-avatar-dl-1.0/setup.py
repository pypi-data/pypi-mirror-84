import setuptools
with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="github-avatar-dl", 
    version="1.0",
    author="Arnav Mehta",
    description="A python module that will allow users to download GitHub avatar images",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/mehtaarn000/github-avatar-dl",
    packages=['github_avatar_dl'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)