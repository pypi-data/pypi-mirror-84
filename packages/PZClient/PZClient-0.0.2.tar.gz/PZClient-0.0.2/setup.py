import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()
setuptools.setup(
    name="PZClient",
    version="0.0.2",
    author="PZStocks",
    author_email="ramperel98@gmail.com",
    description="A client for who wants to integrate with PZStocks",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.com/Ram_and_Zada_stocks/PZClient/",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
