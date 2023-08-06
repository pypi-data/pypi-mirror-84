# CMOT
A collection of miscellaneous goods at an unbeatable price.

This project is a collection of relatively isolated utilities.
They are designed to minimize inter-dependencies such that, if desired, it is
easy to copy only the needed files (and license) instead of importing the whole
project.

## Install
```sh
pip install cmot
```

## Development
### Editable Install
```sh
python setup.py develop [--user]
```
Re-run this command to refresh the version number (based on git tags).

### Versioning
Uses [Semantic Versioning](https://semver.org/).

Versions are set exclusively via git tags:
```sh
git -a v0.1.2 -m ""
```
