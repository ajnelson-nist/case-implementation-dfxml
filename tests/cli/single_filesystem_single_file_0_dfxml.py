#!/usr/bin/env python

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

__version__ = "0.2.0"

import hashlib

from dfxml import objects as Objects


def main() -> None:
    dobj = Objects.DFXMLObject()

    vobj = Objects.VolumeObject()
    dobj.append(vobj)
    fobj = Objects.FileObject()
    vobj.append(fobj)

    vobj.ftype_str = "ntfs"
    vobj.partition_offset = 0

    fobj.filename = "single_file.dat"

    contents = b"AAAA\n"
    fobj.filesize = len(contents)

    _md5er = hashlib.md5()
    _md5er.update(contents)
    fobj.md5 = _md5er.hexdigest()

    _sha1er = hashlib.sha1()
    _sha1er.update(contents)
    fobj.sha1 = _sha1er.hexdigest()

    _sha256er = hashlib.sha256()
    _sha256er.update(contents)
    fobj.sha256 = _sha256er.hexdigest()

    fobj.crtime = "2000-02-03T04:05:06Z"
    fobj.mtime = "2001-02-03T04:05:06Z"
    fobj.atime = "2003-02-03T04:05:06Z"
    fobj.ctime = "2004-02-03T04:05:06Z"

    with open(args.out_dfxml, "w") as out_fh:
        dobj.print_dfxml(output_fh=out_fh)


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("out_dfxml")
    args = parser.parse_args()
    main()
