from setuptools import setup
from setuptools import find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

packages = find_packages()

setup(
    name="oaas_registry_api",
    version="1.2.0",
    description="oaas_registry_api",
    long_description=readme,
    author="Bogdan Mustiata",
    author_email="bogdan.mustiata@gmail.com",
    license="BSD",
    install_requires=[
        "oaas",
        "grpc-stubs==1.24.2",
    ],
    packages=packages,
    package_data={
        "": ["*.txt", "*.rst"],
        "oaas_registry_api": ["py.typed"],
    },
)
