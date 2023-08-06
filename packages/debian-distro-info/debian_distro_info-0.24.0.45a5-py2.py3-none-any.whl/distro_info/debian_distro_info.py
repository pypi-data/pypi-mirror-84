#!/usr/bin/python

# Copyright (C) 2009-2011, Benjamin Drung <bdrung@debian.org>
#
# Permission to use, copy, modify, and/or distribute this software for any
# purpose with or without fee is hereby granted, provided that the above
# copyright notice and this permission notice appear in all copies.
#
# THE SOFTWARE IS PROVIDED "AS IS" AND THE AUTHOR DISCLAIMS ALL WARRANTIES
# WITH REGARD TO THIS SOFTWARE INCLUDING ALL IMPLIED WARRANTIES OF
# MERCHANTABILITY AND FITNESS. IN NO EVENT SHALL THE AUTHOR BE LIABLE FOR
# ANY SPECIAL, DIRECT, INDIRECT, OR CONSEQUENTIAL DAMAGES OR ANY DAMAGES
# WHATSOEVER RESULTING FROM LOSS OF USE, DATA OR PROFITS, WHETHER IN AN
# ACTION OF CONTRACT, NEGLIGENCE OR OTHER TORTIOUS ACTION, ARISING OUT OF
# OR IN CONNECTION WITH THE USE OR PERFORMANCE OF THIS SOFTWARE.

# pylint: disable=invalid-name
# pylint: enable=invalid-name

"""provides information about Debian's distributions"""

import argparse
import os
import sys

from distro_info import convert_date, DebianDistroInfo


def parse_args():
    script_name = os.path.basename(sys.argv[0])
    usage = "%s [options]" % (script_name)
    epilog = "See %s(1) for more info." % (script_name)
    parser = argparse.ArgumentParser(usage=usage, epilog=epilog)

    parser.add_argument("--date", dest="date", default=None,
                        help="date for calculating the version (default: today).")
    parser.add_argument("-a", "--all", dest="all", action="store_true",
                        help="list all known versions")
    parser.add_argument("-d", "--devel", dest="devel", action="store_true",
                        help="latest development version")
    parser.add_argument("-o", "--old", dest="old", action="store_true",
                        help="latest old (stable) version")
    parser.add_argument("-s", "--stable", dest="stable", action="store_true",
                        help="latest stable version")
    parser.add_argument("--supported", dest="supported", action="store_true",
                        help="list of all supported stable versions")
    parser.add_argument("-t", "--testing", dest="testing", action="store_true",
                        help="current testing version")
    parser.add_argument("--unsupported", dest="unsupported",
                        help="list of all unsupported stable versions")

    args = parser.parse_args()

    versions = [args.all, args.devel, args.old, args.stable,
                args.supported, args.testing, args.unsupported]
    if len([x for x in versions if x]) != 1:
        parser.error("You have to select exactly one of --all, --devel, --old, "
                     "--stable, --supported, --testing, --unsupported.")

    if args.date is not None:
        try:
            args.date = convert_date(args.date)
        except ValueError:
            parser.error("Option --date needs to be a date in ISO 8601 "
                         "format.")
    return args


def main():
    args = parse_args()
    if args.all:
        for distro in DebianDistroInfo().all:
            sys.stdout.write(distro + "\n")
    elif args.devel:
        sys.stdout.write(DebianDistroInfo().devel(args.date) + "\n")
    elif args.old:
        sys.stdout.write(DebianDistroInfo().old(args.date) + "\n")
    elif args.stable:
        sys.stdout.write(DebianDistroInfo().stable(args.date) + "\n")
    elif args.supported:
        for distro in DebianDistroInfo().supported(args.date):
            sys.stdout.write(distro + "\n")
    elif args.testing:
        sys.stdout.write(DebianDistroInfo().testing(args.date) + "\n")
    elif args.unsupported:
        for distro in DebianDistroInfo().unsupported(args.date):
            sys.stdout.write(distro + "\n")


if __name__ == "__main__":
    main()
