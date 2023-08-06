import setuptools
import os

with open("README.md") as fd:
    long_description = fd.read()


def get_version():
    with open(
        os.path.join(
            os.path.abspath(os.path.dirname(__file__)), "pylogview", "__version__.py"
        )
    ) as fd:
        for line in fd.readlines():
            if line.startswith("__version__"):
                delim = '"' if '"' in line else "'"
                return line.split(delim)[1]
        else:
            raise RuntimeError("Unable to find version string.")


setuptools.setup(
    name="pylogview",
    version=get_version(),
    author="Michael Murton",
    description=(
        "logview is a simple terminal script that allows you to tail multiple log "
        "files in a windowed format."
    ),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/CrazyIvan359/logview",
    packages=["pylogview"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Environment :: Console :: Curses",
        # "Operating System :: POSIX :: Linux",
        "Programming Language :: Python",
        "Topic :: Home Automation",
        "Topic :: Internet :: Log Analysis",
        "Topic :: System :: Logging",
        "Topic :: Utilities",
    ],
    license="MIT",
    keywords="log, logging, tail",
    install_requires=["blessings>=1.7,<2.0", "datefinder>=0.7.1,<1.0"],
    entry_points={"console_scripts": ["logview=pylogview.__main__:main"]},
    zip_safe=False,
)
