![Automated tests](https://github.com/korpling/graphANNIS-python/workflows/Automated%20tests/badge.svg)

# graphANNIS Python Bindings

GraphANNIS is a library for corpus linguistic queries and these are the Python bindings to **graphANNIS core library version 0.30.0**.


## How to use in your own scripts

GraphANNIS is available as Python3-compatible library from the central PyPI repository: https://pypi.org/project/graphannis/
You can install it locally with *pip* (https://pip.pypa.io/en/stable/).
```
pip install graphannis
```
On Ubuntu Linux systems the command might be `pip3`for Python 3.

You can view the [API documentation online](http://graphannis-python.readthedocs.io/).

## How to compile/install from source

Install you the python packages locally (use Python3) for your current user (remove the `--user` to install it system-wide)
```
python3 setup.py install --user
```

This will automatically download the the graphANNIS binaries to the `graphannis/<platform>` folder, where platform is one of the following:

| Operating system       | `<platform>`  |
|------------------------|---------------|
| Linux (64 bit)         | linux-x86-64  |
| MacOS X (64 bit)       | darwin-x86-64 |
| Windows (64 bit)       | win32-x86-64  |

You can change the `CORE_VERSION` field in the `setup.py` to use a different released version of graphANNIS.

To compile graphANNIS on your own (e.g. for using a non-released version)

- Clone the graphANNIS library  from https://github.com/korpling/graphANNIS/
- Follow the [graphANNIS compile instructions](https://github.com/korpling/graphANNIS#how-to-compile)
- Copy the resulting shared library file `<graphANNIS-repo>/target/release/libgraphannis.so` (`libgraphannis.dylib` under MacOS X and `graphannis.dll` under Windows) into the `graphannis/<platform>` folder.

## Release process

1. Make a new **release branch** `release/<version>` from the `develop` branch for feature releases. If you make a bug-fix release create a branch named `hotfix/<version>` from the `master` branch.
2. **Update version** information, by 
    - changing the `VERSION` field in the `setup.py` file
    - specifying the corresponding graphANNIS release tag in the `CORE_VERSION` field in the `setup.py` file
    - committing the changed files
3. **Prepare the release (including executing tests)** by executing `./release_prepare.sh`.
4. Check if there where no test errors and **Commit** the changes created by release preparation script.
5. **Tag and push** the latest commit with the prefix `v`, e.g. `v1.4.0`, **merge** the release branch both into the `master` and `develop` branch then delete the release branch.

CI will automatically deploy all released versions on the `master` branch.

## 3rd party dependencies

- CFFI (http://cffi.readthedocs.org/) MIT License
- networkX (http://networkx.github.io/) BSD License

## Author(s)

* Thomas Krause (thomaskrause@posteo.de)
