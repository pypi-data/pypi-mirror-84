from setuptools import setup, find_packages
import pathlib

here = pathlib.Path(__file__).parent.resolve()

# Get the long description from the README file
long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="boondh",
    version="0.1.4",
    description="A Swiss Knife",
    long_description=long_description,
    long_description_content_type="text/markdown",
    keywords=["utility", "data", "multiprocessing", "cli", "tools"],
    url="https://github.com/rohit-mehra/boondh",
    author="Rohit Mehra",
    author_email="iirohitmehra@gmail.com",
    package_dir={"": "src"},
    packages=find_packages("src"),
    install_requires=[
        "numpy",
        # dataclasses for Python versions that don't have it
        'dataclasses;python_version<"3.7"',
        # utilities from PyPA to e.g. compare versions
        "packaging",
        # progress bars
        "tqdm >= 4.27",
        # data ops
        "pandas",
    ],
    python_requires=">=3.6.0",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development",
    ],
)

