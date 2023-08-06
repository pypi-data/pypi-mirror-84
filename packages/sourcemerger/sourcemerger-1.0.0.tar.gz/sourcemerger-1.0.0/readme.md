<div align="center">
    <img src="https://gitlab.com/russofrancesco/sourcemerger/-/raw/master/media/artwork/sourcemerger_logo.jpg" width="250" alt="sourcemerger-logo">
    <h1>sourcemerger</h1>
    <p>
        <b>Single-header C++ library generator</b>
    </p>
    <a href="https://gitlab.com/russofrancesco/sourcemerger/-/commits/master"><img src="https://gitlab.com/russofrancesco/sourcemerger/badges/master/pipeline.svg?job=karma&key_text=tests&key_width=39" alt="tests-badge"></a>
    <a href="https://gitlab.com/russofrancesco/sourcemerger/-/commits/master"><img src="https://gitlab.com/russofrancesco/sourcemerger/badges/master/coverage.svg" alt="coverage-badge"></a>
    <a href="https://img.shields.io/badge/license-MIT-informational"><img src="https://img.shields.io/badge/license-MIT-informational"></a>
    <br>
    <br>
</div>

sourcemerger is a Python command-line tool that generates a single-header C++ library from your source code.\
It takes as input your headers and implementation files and outputs one .h file (with include guards) and one .cpp file.

## Quickstart
### Requirements

You'll need [Python 3.6 or newer](https://www.python.org/).

### Install

sourcemerger is installed via pip, the Python package installer:
```
pip install sourcemerger
```

### Usage

Point sourcemerger to the headers and implementation files of your library, choose what name to give to the two output files and specify a destination folder:
```
sourcemerger -e path/to/your/headers -s path/to/your/impl_files -n your_library_name -d path/to/destination
```

## Options
```
-e, --headers HEADERS_FOLDER        Path to the folder that contains the headers (both .h and .hpp headers are supported)
-s, --sources IMPL_FOLDER           Path to the folder that contains the implementation files (i.e. the .cpp files)
-n, --name LIBRARY_NAME             Name of the output library files (.h and .cpp extensions are appended automatically)
-d, --dest DEST_FOLDER              Path to save the output files in (optional; default is current dir)
-v, --verbose                       Enable verbose output
-h, --help                          Show this help message and exit
--version                           Show version number and exit
```

## Versioning

sourcemerger uses [Semantic Versioning](https://semver.org/).

## Public API

As per semver requirements, the public API of sourcemerger is hereby declared as consisting of:
* its [command-line options](#options);
* its top-level function ``merge_files``, which you may import into your project (e.g. ``from sourcemerger import merge_files``).

## License

sourcemerger is released under [MIT license](https://gitlab.com/russofrancesco/sourcemerger/-/blob/master/license.txt).
