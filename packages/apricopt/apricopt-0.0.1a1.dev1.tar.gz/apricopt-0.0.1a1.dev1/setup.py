import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="apricopt",
    version="0.0.1a1.dev1",
    author="Marco Esposito",
    author_email="esposito@di.uniroma1.it",
    description="A library for simulation-based parameter optimization",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="http://mclab.di.uniroma1.it",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU Lesser General Public License v3 (LGPLv3)",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)