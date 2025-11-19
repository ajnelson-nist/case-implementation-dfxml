# CASE/UCO DFXML implementation

[![Continuous Integration](https://github.com/casework/CASE-Implementation-Template-Python-CLI/actions/workflows/ci.yml/badge.svg)](https://github.com/casework/CASE-Implementation-Template-Python-CLI/actions/workflows/ci.yml)
![CASE Version](https://img.shields.io/badge/CASE%20Version-1.4.0-green)

_(Please see the [NIST disclaimer](#disclaimer).)_

This repository implements translations between Digital Forensics XML ([DFXML](http://forensicswiki.org/wiki/Category:Digital_Forensics_XML)) and Cyber-investigation Analysis Standard Expression ([CASE](https://caseontology.org/)).


## Installation

This repository provides two commands on installation.  It depends on the [CASE Python Utilities](https://github.com/casework/CASE-Utilities-Python) being installed (which can be done via `pip`), and the [DFXML Python library](https://github.com/dfxml-working-group/dfxml_python).  These installations can be done in a virtual environment if you do not have (or wish to use) administrator privileges.

Running "`make check`" creates a usable virtual environment under `tests/venv`, as well as running unit tests.  This will require networking to install any dependencies not yet cached by `pip`.


## Usage

Translating DFXML to CASE:

    dfxml_to_case input.dfxml output.case

(`dfxml_to_case.py` allows output format selection with `--output-format`.  Default is TTL.)

Translating CASE to DFXML:

    case_to_dfxml input.case output.dfxml

If pretty-printing the XML output is desired, you may want to pipe through `xmllint`:

    case_to_dfxml input.case >(xmllint --format - > output.dfxml)


### Testing

There is a set of unit tests that checks round-trip conversion between the formats.  Note that DFXML and CASE do not have the same conceptual scope, so the tests only cover translation in the context of storage system metadata.

Unit tests run with `make check`, without requiring administrator privileges (though may require networking as under the "Installation" section).


#### Make targets

Some `make` targets are defined for this repository:

* `all` - Installs `pre-commit` for this cloned repository instance.
* `check` - Run unit tests.  *NOTE*: The tests entail an installation of this project's source tree, including prerequisites downloaded from PyPI.
* `clean` - Remove test build files.


## Versioning

This repository follows [SEMVER](https://semver.org/) conventions on a per-script basis.  Version 0.1.0 will start providing a stable API, but currently awaits a CASE validation mechanism.


## Licensing

Portions of this repository contributed by NIST are governed by the [NIST Software Licensing Statement](LICENSE#nist-software-licensing-statement).


## Disclaimer

Participation by NIST in the creation of the documentation of mentioned software is not intended to imply a recommendation or endorsement by the National Institute of Standards and Technology, nor is it intended to imply that any specific software is necessarily the best available for the purpose.
