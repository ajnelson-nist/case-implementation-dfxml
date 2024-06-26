#!/usr/bin/env python3

# Portions of this file contributed by NIST are governed by the
# following statement:
#
# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the course
# of their official duties. Pursuant to Title 17 Section 105 of the
# United States Code, this software is not subject to copyright
# protection within the United States. NIST assumes no responsibility
# whatsoever for its use by other parties, and makes no guarantees,
# expressed or implied, about its quality, reliability, or any other
# characteristic.
#
# We would appreciate acknowledgement if the software is used.

# TODO - Adapt below.

"""
case_cli_example is a command that demonstrates making a CLI application tested with a Make-based workflow.
"""

__version__ = "0.0.1"


def foo() -> str:
    """
    This function is provided to demonstrate the doctests system templated in this repository.  If all doctests from the package source directory are removed, the 'check-doctest' recipe in /tests/Makefile will also need to be removed, because pytest reports a failure if no tests are found.

    >>> foo()
    'x'
    """
    return "x"
