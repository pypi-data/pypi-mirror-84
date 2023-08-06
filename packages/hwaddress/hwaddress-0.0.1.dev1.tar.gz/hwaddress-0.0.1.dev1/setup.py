"""Setup hwaddress."""

import setuptools

with open("README.rst", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="hwaddress",
    version='0.0.1.dev1',
    author="Eric Geldmacher",
    author_email="egeldmacher@wustl.edu",
    description="Lightweight EUI-48/64 based hardware (MAC) address library.",
    long_description=long_description,
    url="https://github.com/ericgeldmacher/hwaddress",
    license="MIT",
    packages=['hwaddress'],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
