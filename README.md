# CASE Implementation Template: CLI Example

[![Continuous Integration](https://github.com/casework/CASE-Implementation-Template-Python-CLI/actions/workflows/ci.yml/badge.svg)](https://github.com/casework/CASE-Implementation-Template-Python-CLI/actions/workflows/ci.yml)
![CASE Version](https://img.shields.io/badge/CASE%20Version-1.3.0-green)

_(Please see the [NIST disclaimer](#disclaimer).)_

This template repository is provided for those looking to develop command-line utilities using ontologies within the [Cyber Domain Ontology](https://cyberdomainontology.org) ecosystem, particularly [CASE](https://caseontology.org) and [UCO](https://unifiedcyberontology.org).

This template repository provides a [Make](https://en.wikipedia.org/wiki/Make_%28software%29)-based test workflow used in some other CASE projects.  The workflow exercises this project as a command-line interface (CLI) application (under [`tests/cli/`](tests/cli/)), and as a package (under [`tests/package/`](tests/package/)).

This is only one possible application development style, and templates are available to support other styles.  See for instance:

* [casework/CASE-Mapping-Template-Python](https://github.com/casework/CASE-Mapping-Template-Python), which demonstrates an approach based on constructing Python `dict`s and checking generated results afterwards for CASE conformance with the [CASE Validation Action](https://github.com/kchason/case-validation-action).

Testing procedures run in _this_ repository are:

* _GitHub Actions_: [Workflows](.github/workflows/) are defined to run testing as they would be run in a local command-line environment, reviewing on pushes and pull requests to certain branches.
* _Supply chain review_: [One workflow](.github/workflows/supply-chain.yml) checks dependencies on a schedule, confirming pinned dependencies are the latest, and loosely-pinned dependencies do not impact things like type review.
* _Type review_: `mypy --strict` reviews the package source tree and the tests directory.
* _Code style_: `pre-commit` reviews code patches in Continuous Integration testing and in local development.  Running `make` will install `pre-commit` in a special virtual environment dedicated to the cloned repository instance.
* _Doctests_: Module docstrings' inlined tests are run with `pytest`.
* _CASE validation_: Unit tests that generate CASE graph files are written to run `case_validate` before considering the file "successfully" built.
* _Editable package installation_: The test suite installs the package in an "editable" mode into the virtual environment under `tests/venv/`.  Activating the virtual environment (e.g. for Bash users, running `source tests/venv/bin/activate` from the repository's top source directory) enables "live code" testing.
* _Parallel Make runs_: Tests based on `make` have dependencies specified in a manner that enables `make --jobs` to run testing in parallel.
* _Directory-local Make runs_: The Makefiles are written to run regardless of the present working directory within the top source directory or the [`tests/`](tests/) directory, assuming `make check` has been run from the top source directory at least once.  If a test is failing, `cd`'ing into that test's directory and running `make check` should reproduce the failure quickly and focus development effort.


## Usage

To use the template, push the "Use this template" button on GitHub, and adapt files as suits your new project's needs.  The README should be revised at least from its top to the "Versioning" section.  Source files should be renamed and revised, and any other files with a `TODO` within it should be adjusted.

After any revisions, running `make check` (or `make -j check`) from the top source directory should have unit tests continue to pass.

_Below this line is sample text to use and adapt for your project.  Most text above this line is meant to document the template, rather than projects using the template._

To install this software, clone this repository, and run `pip install .` from within this directory.  (You might want to do this in a virtual environment.)

This provides a standalone command:

```bash
case_cli_example output.rdf
```

The tests build several examples of output for the command line mode, under [`tests/cli`](tests/cli/).

The installation also provides a package to import:

```python
import case_cli_example
help(case_cli_example.foo)
```


## Versioning

This project follows [SEMVER 2.0.0](https://semver.org/) where versions are declared.


## Make targets

Some `make` targets are defined for this repository:
* `all` - Installs `pre-commit` for this cloned repository instance.
* `check` - Run unit tests.  *NOTE*: The tests entail an installation of this project's source tree, including prerequisites downloaded from PyPI.
* `clean` - Remove test build files.


## Licensing

This repository is licensed under the Apache 2.0 License. See [LICENSE](LICENSE).

Portions of this repository contributed by NIST are governed by the [NIST Software Licensing Statement](THIRD_PARTY_LICENSES.md#nist-software-licensing-statement).


## Disclaimer

Participation by NIST in the creation of the documentation of mentioned software is not intended to imply a recommendation or endorsement by the National Institute of Standards and Technology, nor is it intended to imply that any specific software is necessarily the best available for the purpose.
