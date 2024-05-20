from setuptools import setup, find_packages


def get_requirements(source):
    """Get the requirements from the given ``source``

    Parameters
    ----------
    source: str
        The filename containing the requirements

    """
    with open(source, "r") as f:
        requirements = f.read().splitlines()

    return requirements


setup(
    packages=find_packages(),
    install_requires=get_requirements("requirements/requirements.txt")
)
