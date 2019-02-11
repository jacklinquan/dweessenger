from setuptools import setup

setup(
    name="dweessenger",
    version="0.1.0",
    description="A simple python package for messaging through free dweet " + \
        "service.",
    long_description="https://github.com/jacklinquan/dweessenger",
    long_description_content_type="text/markdown",
    url="https://github.com/jacklinquan/dweessenger",
    author="Quan Lin",
    author_email="jacklinquan@gmail.com",
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3"
    ],
    packages=["dweessenger"],
    install_requires=["cryptodweet"]
)
