import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="linuxvoice", # Replace with your own username
    version="1.3.2",
    author="Jeffrin Jose T",
    author_email="jeffrin@rajagiritech.edu.in",
    description="A small package for downloading LINUXVOICE issues",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ahiliation/DOLLECT",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
