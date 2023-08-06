import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="aCrypt",
	version="0.1.7",
    author="ChezCoder",
    author_email="mrpizzaguyytb@gmail.com",
    description="Ciphering made easy.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://repl.it/@ChezCoder/aCrypt",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 2",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)