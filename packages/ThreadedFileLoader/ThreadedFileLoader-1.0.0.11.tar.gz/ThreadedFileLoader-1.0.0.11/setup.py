import pathlib
from setuptools import setup

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

with open("minor_version", "r") as afile:
    minor_version = afile.readline()


# This call to setup() does all the work
setup(
    name="ThreadedFileLoader",
    version=f"1.0.0.{minor_version}",
    description="",
    long_description=README,
    long_description_content_type="text/markdown",
    url="https://QuantumNovice.github.io/ThreadedFileLoader",
    author="QuantumNovice",
    author_email="portabl3lapy@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
    ],
    packages=["ThreadedFileLoader"],
    include_package_data=True,
    install_requires=["imageio", "wheel"],
    # entry_points={"console_scripts": ["pip-grab=pip-grab.__main__:main",]},
    python_requires=">=3.6",
)

with open("minor_version", "w") as afile:
    afile.write(str(int(minor_version) + 1))


