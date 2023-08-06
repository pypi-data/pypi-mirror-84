import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="sphinx-veldus-ext", # Replace with your own username
    version="0.1.0",
    author="Adam DuQuette",
    author_email="duquetteadam@gmail.com",
    description="A Sphinx Extension built for Veldus",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/dukeofetiquette/sphinx-veldus-ext",
    packages=setuptools.find_packages(),
    package_data={'veldus_ext': ['templates/*.html']},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)