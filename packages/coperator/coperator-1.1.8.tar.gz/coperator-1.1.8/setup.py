from setuptools import setup  # type: ignore

# read the contents of your README file

with open("README.rst", "r") as readme_file:
    readme = readme_file.read()


setup(
    name="coperator",
    version="1.1.8",
    description="Custom operators for python",
    long_description=readme,
    author="Jean Carlo Jimenez Giraldo",
    author_email="mandalarotation@gmail.com",
    url="https://gitlab.com/jecjimenezgi/coperator.git",
    package_data={"coperator": ["py.typed", "coperator.pyi"]},
    packages=["coperator"],
    scripts=[],
    install_requires=["typing"],
)
