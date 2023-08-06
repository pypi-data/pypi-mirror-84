from setuptools import setup  # type: ignore

setup(
    name="coperator",
    version="1.1.2",
    description="Custom operators for python",
    author="Jean Carlo Jimenez Giraldo",
    author_email="jecjimenezgi@unal.edu.co\nmandalarotation@gmail.com",
    url="https://gitlab.com/jecjimenezgi/coperator.git",
    package_data={"coperator": ["py.typed", "coperator.pyi"]},
    packages=["coperator"],
    scripts=[],
    install_requires=["typing"],
)
