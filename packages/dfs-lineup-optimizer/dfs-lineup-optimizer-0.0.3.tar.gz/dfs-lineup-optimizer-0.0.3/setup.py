from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    install_requires=[
        "amply==0.1.4; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "certifi==2020.6.20",
        "chardet==3.0.4",
        "docutils==0.16; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4'",
        "idna==2.10; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3'",
        "pulp==2.3.1",
        "pyparsing==2.4.7; python_version >= '2.6' and python_version not in '3.0, 3.1, 3.2'",
        "requests==2.24.0",
        "urllib3==1.25.11; python_version >= '2.7' and python_version not in '3.0, 3.1, 3.2, 3.3, 3.4' and python_version < '4'",
    ],
    name="dfs-lineup-optimizer",
    version="0.0.3",
    author="Aaron Mamparo",
    author_email="aaronmamparo@gmail.com",
    description="Generate optimal DFS lineups",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/amamparo/dfs-lineup-optimizer",
    package_dir={"": "src"},
    packages=find_packages("src"),
    entry_points={"console_scripts": ["dfslo = dfslo.get_data:main"]},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">= 3.8",
)
