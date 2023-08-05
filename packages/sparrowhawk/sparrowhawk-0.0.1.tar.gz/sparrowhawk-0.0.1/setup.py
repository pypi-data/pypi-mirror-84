import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sparrowhawk",
    version="0.0.1",
    author="vcokltfre",
    author_email="vcokltfre@gmail.com",
    description="A bot builder for discord.py",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/vcokltfre/sparrowhawk",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)