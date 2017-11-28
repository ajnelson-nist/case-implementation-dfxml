# CASE/UCO DFXML implementation

This repository implements translations between Digital Forensics XML ([DFXML](http://forensicswiki.org/wiki/Category:Digital_Forensics_XML)) and Cyber-investigation Analysis Standard Expression ([CASE](https://casework.github.io/case/)).


## Caveats

This repository does not yet validate generated CASE data against CASE and the [Unified Cyber Ontology](https://ucoproject.github.io/uco/).


## Install

This repository runs as in-place scripts.  It depends on the [CASE Python API](https://github.com/casework/case-api-python) being installed according to that repository's README, which is doable in a virtual environment if you do not have (or wish to use) administrator priveleges.

You can run "`make setup`" to create a usable virtual environment under `./venv`.  This will require networking to install any dependencies not yet cached by `pip`.


## Usage

Translating DFXML to CASE:

    python dfxml_to_case.py input.dfxml output.case

(`dfxml_to_case.py` allows output format selection with `--output-format`.  Default is TTL.)

Translating CASE to DFXML:

    python case_to_dfxml.py input.case output.dfxml

If pretty-printing the XML output is desired, you may want to pipe through `xmllint`:

    python case_to_dfxml.py input.case >(xmllint --format - > output.dfxml)


### Testing

There is a set of unit tests that checks round-trip conversion between the formats.  Note that DFXML and CASE do not have the same conceptual scope, so the tests only cover translation in the context of storage system metadata.

Unit tests run with `make check`, without requiring administrator privileges (though may require networking as under the "Install" section).


## Versioning

This repository follows [SEMVER](https://semver.org/) conventions on a per-script basis.  Version 0.1.0 will start providing a stable API, but currently awaits a CASE validation mechanism.


## License

Public domain.  See [LICENSE](LICENSE).
