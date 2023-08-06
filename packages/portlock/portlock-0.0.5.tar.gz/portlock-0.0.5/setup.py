import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="portlock",
    version="0.0.5",
    author="Kapil Yedidi",
    author_email="kapily.code@gmail.com",
    description="A package to lock ports",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/kapily/portlock",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.0',
)
