from os import path

from setuptools import setup, find_packages

__version__ = None
exec(open(path.join(path.dirname(__file__), "./yabu/version.py")).read())
if __version__ == "dev":
    __version__ = "0.0"

with open(path.join(path.dirname(__file__), "README.md")) as f:
    _LONG_DESCRIPTION = f.read()

setup(
    name="yabu",
    packages=find_packages(),
    version=__version__,
    license="gpl-3.0",
    description="yet another backup utility",
    long_description=_LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    author="Roberto Bochet",
    author_email="robertobochet@gmail.com",
    url="https://github.com/RobertoBochet/yabu",
    keywords=["backup", "rsync"],
    install_requires=[
        "yamale ~= 3.0.4",
        "PyYAML~=5.3.1"
    ],
    package_data={
        "yabu.resources": ["config.schema.yaml"]
    },
    data_files=[
        ("", [
            "config.example.yaml",
            "utilities/systemd_units/yabu.service",
            "utilities/systemd_units/yabu.timer"
        ])
    ],
    classifiers=[
        "Development Status :: 2 - Pre-Alpha",
        "Intended Audience :: System Administrators",
        "Operating System :: POSIX :: Linux",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Programming Language :: Python :: 3"
    ],
    python_requires=">=3.8"
)
