from setuptools import setup, find_packages

setup(
    name="yarl",
    version="1.0a",
    description="Chocopy compiler package",
    package_dir={"":"include"},
    packages=find_packages("include")
)
