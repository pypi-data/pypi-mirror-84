from setuptools import setup

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name='ablpywrapper',
    version='0.0.1',
    description='Astro botlist python api wrapper',
    py_modules=["main"],
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Operating System :: OS Independent"
    ],
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
      "requests"
    ],
    extras_require={
        "dev": [
            "pytest>=3.7"
        ]
    },
    url="https://github.com/botlists/ablpywrapper",
    author="Sell"
)
