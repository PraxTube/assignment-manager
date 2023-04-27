from setuptools import setup, find_packages
import pathlib


here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")


setup(
    name="assignment-manager",
    version="0.1.4",
    description=("Manage reoccuring assignments and tasks."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/PraxTube/assignment-manager",
    author="Prax",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3 :: Only",
    ],
    keywords="manager, task, assignment, task-manager, assignment-manager",
    package_dir={"": "src"},
    # You can just specify package directories manually here if your project is
    # simple. Or you can use find_packages().
    packages=find_packages(where="src"),
    include_package_data=True,
    python_requires=">=3.8, <4",
    install_requires=["rich", "typer", "inquirer"],
    # List additional groups of dependencies here (e.g. development
    # dependencies). Users will be able to install these using the "extras"
    # syntax, for example:
    #
    #   $ pip install sampleproject[dev]
    #
    # Similar to `install_requires` above, these must be valid existing
    # projects.
    # extras_require={
    #    "dev": ["check-manifest"],
    #    "test": ["coverage"],
    # },
    # Entry points. The following would provide a command called `sample` which
    # executes the function `main` from this package when invoked:
    entry_points={
        "console_scripts": [
            "assman=assignment_manager:main.main",
            "assignment-manager=assignment_manager:main.main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/PraxTube/assignment-manager/issues",
        "Source": "https://github.com/PraxTube/assignment-manager",
    },
)
