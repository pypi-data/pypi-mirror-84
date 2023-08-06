from setuptools import setup
from setuptools import find_packages

with open("README.rst") as readme_file:
    readme = readme_file.read()

packages = find_packages()

setup(
    name="oaas_simple",
    version="1.3.0",
    description="oaas_simple",
    long_description=readme,
    author="Bogdan Mustiata",
    author_email="bogdan.mustiata@gmail.com",
    license="BSD",
    install_requires=[
        "grpcio",
        "oaas",
        "grpc-stubs==1.24.2",
        "oaas-registry-api",
        "oaas-grpc",
    ],
    packages=packages,
    package_data={
        "": ["*.txt", "*.rst"],
        "oaas_simple": ["py.typed"],
    },
)
