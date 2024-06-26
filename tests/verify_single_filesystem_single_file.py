#!/usr/bin/env python

# This software was developed at the National Institute of Standards
# and Technology by employees of the Federal Government in the course
# of their official duties. Pursuant to title 17 Section 105 of the
# United States Code this software is not subject to copyright
# protection and is in the public domain. NIST assumes no
# responsibility whatsoever for its use by other parties, and makes
# no guarantees, expressed or implied, about its quality,
# reliability, or any other characteristic.
#
# We would appreciate acknowledgement if the software is used.

__version__ = "0.1.0"

import logging
import os

import Objects

_logger = logging.getLogger(os.path.basename(__file__))


def main():
    volumeobject_count = 0
    fileobject_count = 0
    for event, obj in Objects.iterparse(args.in_dfxml):
        if event != "end":
            continue
        if isinstance(obj, Objects.VolumeObject):
            volumeobject_count += 1
            if len(obj.annos) > 0:
                _logger.info("obj.annos: %r." % obj.annos)
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
                _logger.info(
                    "%s: %r -> %r."
                    % (diff, getattr(obj, diff), getattr(obj.original_fileobject, diff))
                )
            raise ValueError(
                "Information changed translating between DFXML, CASE, and back."
            )
    if volumeobject_count == 0:
        raise ValueError("No file systems emitted.")
    if fileobject_count == 0:
        raise ValueError("No files emitted.")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("-d", "--debug", action="store_true")
    parser.add_argument("in_dfxml")
    args = parser.parse_args()
    logging.basicConfig(level=logging.DEBUG if args.debug else logging.INFO)
    main()
