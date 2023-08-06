from setuptools import setup  # type: ignore

# read the contents of your README file

with open("README.md", "r") as fh:
    long_description = fh.read()


setup(
    name="coperator",
    version="1.1.4",
    description="Custom operators for python",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Jean Carlo Jimenez Giraldo",
    author_email="jecjimenezgi@unal.edu.co\nmandalarotation@gmail.com",
    url="https://gitlab.com/jecjimenezgi/coperator.git",
    package_data={"coperator": ["py.typed", "coperator.pyi"]},
    packages=["coperator"],
    scripts=[],
    install_requires=["typing"],
)
