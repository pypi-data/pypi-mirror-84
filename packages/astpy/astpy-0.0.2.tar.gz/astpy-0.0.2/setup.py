import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="astpy", # Replace with your own username
    version="0.0.2",
    author="Mohamad Anton Setiazi",
    author_email="antons899@gmail.com",
    description="A standard library python package",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/antonsetiazi/astpy_package",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)