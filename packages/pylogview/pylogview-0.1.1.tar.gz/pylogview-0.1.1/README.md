# logview

[![Latest Version](https://img.shields.io/github/v/tag/CrazyIvan359/logview?label=release)](https://github.com/CrazyIvan359/logview/releases)
[![License](https://img.shields.io/badge/license-MIT-green)](https://github.com/CrazyIvan359/logview/blob/master/LICENSE)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

logview is a simple terminal script that allows you to tail multiple log files
in a windowed format.

## Installing

At this time I have only tested with Python 3.8.5 but it should work with all versions.

With pip:

```bash
pip install --user pylogview
```

With setup.py:

```bash
git clone https://github.com/CrazyIvan359/logview.git
cd logview
python setup.py install --user
```

## Usage

Run `logview -h` for full usage details.

![logview screenshot](https://github.com/CrazyIvan359/logview/blob/master/screenshot.png)
