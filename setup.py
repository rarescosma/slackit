from codecs import open
from os import path

from setuptools import setup

PROJECT = "slackit"
DOT = path.abspath(path.dirname(__file__))

# get the dependencies and installs
with open(path.join(DOT, "requirements.txt"), encoding="utf-8") as f:
    all_reqs = f.read().split("\n")

install_requires = [x.strip() for x in all_reqs if "git+" not in x]
dependency_links = [
    x.strip().replace("git+", "") for x in all_reqs if x.startswith("git+")
]

setup(
    name=PROJECT,
    packages=[PROJECT],
    package_data={PROJECT: ["py.typed"]},
    version="0.3.7",
    description="Automate myself",
    author="Rareș Cosma",
    author_email="rares@getbetter.ro",
    url=f"https://github.com/rarescosma/{PROJECT}",
    license="MIT",
    zip_safe=False,  # mypy needs this to be able to find the package
    entry_points={
        "console_scripts": [
            f"{PROJECT} = {PROJECT}.__main__:main",
            f"roamconfig = {PROJECT}.roam:main",
        ]
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Natural Language :: English",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
    ],
    install_requires=install_requires,
    dependency_links=dependency_links,
)
