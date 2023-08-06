import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="bae0n-utils", # Replace with your own username
    version="0.0.6",
    author="Aeon Williams",
    author_email="aeonwilliams@gmail.com",
    description="Utility functions to be used in Python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="",
    packages=setuptools.find_packages(),
    install_requires=[
        'PIL','globimport', 'os', 'pathlib'
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=2.7',
)