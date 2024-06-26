# Test suite

This directory houses proof-of-functionality tests.
* [`gtime_log/`](gtime_log/) - Uses scripts in source tree to build a UCO Process object in a JSON-LD file, using only a GNU Time log file.  Uses a virtual environment built without installing `case_gnu_time`.
* [`gtime_and_done_log/`](gtime_and_done_log/) - As `gtime_log/`, but using a timestamp recorded in another file tied to a process output.
* [`from_pip/`](from_pip/) - Uses virtual environment with the package `case_gnu_time` installed.  (Runs [`setup.py`](../setup.py), not `pip install`.)  Runs program `case_gnu_time`, producing a Process as in `gtime_log`.
* [`as_import/`](as_import/) - Uses `case_gnu_time` as an imported package to create a custom-named UCO `CyberItem` with a Process Facet.


## Running the test suite

Run `make check`.  `make check` should be run from one directory up, at least once, to trigger some downloads.
