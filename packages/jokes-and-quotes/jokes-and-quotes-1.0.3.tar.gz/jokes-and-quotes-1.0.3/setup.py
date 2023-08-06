from setuptools import setup

def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name="jokes-and-quotes",
    version="1.0.3",
    description="A Python package to get some awesome jokes and quotes.",
    long_description=readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/pinakipb2/jokes-and-quotes",
    author="Pinaki Bhattacharjee",
    author_email="pinakipb2@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
    ],
    packages=["jokes_and_quotes"],
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "jokes-and-quotes=jokes_and_quotes.cli:main",
        ]
    },
)