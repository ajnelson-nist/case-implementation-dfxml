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

import logging
from pathlib import Path

import pytest
from dfxml import objects as Objects


@pytest.mark.parametrize(
    ["in_dfxml"],
    [
        # Verify a DFXML file that just lists a single file can translate into CASE and back via some format.
        ("single_file_0_2_deltas.dfxml",),
        # Verify a DFXML file that just lists a single file can translate into CASE and back via JSON-LD.
        ("single_file_0_json_2_deltas.dfxml",),
    ],
)
def test_single_file_round_trip(in_dfxml: str) -> None:
    srcdir = Path(__file__).parent
    fileobject_count = 0
    for event, obj in Objects.iterparse(str(srcdir / in_dfxml)):
        if event != "end":
            continue
        if not isinstance(obj, Objects.FileObject):
            continue
        fileobject_count += 1
        if "new" in obj.annos:
            raise ValueError("A new file was created in translation.")
        if "deleted" in obj.annos:
            raise ValueError("A file was lost in translation.")
        if len(obj.diffs) > 0:
            for diff in obj.diffs:
                logging.info(
                    "%s: %r -> %r."
                    % (diff, getattr(obj, diff), getattr(obj.original_fileobject, diff))
                )
            raise ValueError(
                "Information changed translating between DFXML, CASE, and back."
            )
    assert fileobject_count > 0, "No files emitted."


def test_single_filesystem_single_file_round_trip() -> None:
    srcdir = Path(__file__).parent
    volumeobject_count = 0
    fileobject_count = 0
    for event, obj in Objects.iterparse(
        str(srcdir / "single_filesystem_single_file_0_2_deltas.dfxml")
    ):
        if event != "end":
            continue
        if isinstance(obj, Objects.VolumeObject):
            volumeobject_count += 1
            if len(obj.annos) > 0:
                logging.info("obj.annos: %r." % obj.annos)
                raise ValueError(
                    "Properties of the file system changed in the round trip."
                )
            continue
        if not isinstance(obj, Objects.FileObject):
            continue
        fileobject_count += 1
        if "new" in obj.annos:
            raise ValueError("A new file was created in translation.")
        if "deleted" in obj.annos:
            raise ValueError("A file was lost in translation.")
        if len(obj.diffs) > 0:
            for diff in obj.diffs:
                logging.info(
                    "%s: %r -> %r."
                    % (diff, getattr(obj, diff), getattr(obj.original_fileobject, diff))
                )
            raise ValueError(
                "Information changed translating between DFXML, CASE, and back."
            )
    assert volumeobject_count > 0, "No file systems emitted."
    assert fileobject_count > 0, "No files emitted."
