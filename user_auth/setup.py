from setuptools import find_packages, setup


def read_requirements(path: str):
    with open(path) as f:
        return f.read().split("\n")


setup(
    name="user_auth",
    version="0.0.1",
    description="user service",
    packages=find_packages(),
    include_package_data=True,
    zip_safe=False,
    install_requires=read_requirements("requirements.txt"),
)
