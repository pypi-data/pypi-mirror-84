from setuptools import setup

from os import path

def get_long_description():
    with open(
        path.join(path.dirname(path.abspath(__file__)), "README.md"),
        encoding="utf8",
    ) as fp:
        return fp.read()


setup(
    name="nbcelldiff",
    author="Tony Hirst",
    author_email="tony.hirst@open.ac.uk",
    description="Tools for finding the difference between two notebook code cells",
    long_description=get_long_description(),
    long_description_content_type="text/markdown",
    url="https://github.com/innovationOUtside/nb_cell_diff",
    packages=['nbcelldiff'],
    license='MIT License',
    package_data = {},
    include_package_data=False,
    install_requires=[],
)