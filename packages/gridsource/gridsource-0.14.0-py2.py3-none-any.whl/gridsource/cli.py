# -*- coding: utf-8 -*-

"""Console script for gridsource.

Command-Line Usage
==================

Although `gridsource` is mainly a library, it also has a small
CLI interface.
"""
import argparse
import os
import pprint
import sys

import pandas as pd

from gridsource import Data, IOData, ValidData, __version__


def version(args=None):
    msg = "gridsource version %s" % __version__
    if args.verbose is True:
        msg += "\n  * Python Version: %s" % sys.version
        msg += "\n  * Python: %s" % sys.executable
        msg += "\n  * Pandas: %s" % pd.__version__
    print(msg)


def format(args):
    """convert file inplace into its own extension"""
    data = IOData()
    data.read(args.input, engine=args.engine)
    data.to(args.input)
    print('formatted "%s"' % args.input)
    return 0


def convert(args):
    """convertion command processor"""
    if args.schema is None:
        # create a non-validating IO class only
        data = IOData()
    else:
        # Data features IO and Validation
        data = Data()
    data.read(args.input, engine=args.engine)
    if args.schema:
        data.read_schema(args.schema)
        report = data.validate()
        if len(report) > 0:
            print("{:-^60}".format(" [Validation Errors] "))
            pprint.pprint(report, width=60)  # TODO: remove me!
            print(60 * "-")
            nb_errors = 0
            for tabname, data in report.items():
                for colrows, errors in data.items():
                    nb_errors += len(errors)
            return 1
    if args.output:
        output = args.output
    else:
        input, ext = os.path.splitext(args.input)
        if ext == ".xlsx":
            target_ext = ".ini"
        if ext in (".cfg", ".ini"):
            target_ext = ".xlsx"
        output = input + target_ext
    data.to(output)
    print('wrote "%s"' % output)
    return 0


def parse_args(args):
    """Console script"""
    # https://docs.python.org/3/library/argparse.html
    # https://docs.python.org/3/howto/argparse.html
    parser = argparse.ArgumentParser("easy CLI for app_name")
    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Show Version and exit"
    )
    parser.set_defaults(process=version)
    # ========================================================================
    # subparsers
    # ========================================================================
    subparsers = parser.add_subparsers(help="sub-command help")
    # ------------------------------------------------------------------------
    # create the parser for the "a" command
    parser_convert = subparsers.add_parser("convert", help="convert")
    parser_convert.add_argument("input", type=str, help="path to input file")
    parser_convert.add_argument("-o", "--output", type=str, help="path to output file")
    parser_convert.add_argument("-s", "--schema", type=str, help="validation schema")
    parser_convert.add_argument(
        "-e",
        "--engine",
        type=str,
        default="xlrd",
        choices=("xlrd", "openpyxl"),
        help="pandas XLSX reader engine",
    )
    parser_convert.set_defaults(process=convert)
    # ------------------------------------------------------------------------
    # inplace formatting
    parser_format = subparsers.add_parser("format", help="format file inplace")
    parser_format.add_argument("input", type=str, help="path to input file")
    parser_format.add_argument(
        "-e",
        "--engine",
        type=str,
        default="xlrd",
        choices=("xlrd", "openpyxl"),
        help="pandas XLSX reader engine",
    )
    parser_format.set_defaults(process=format)

    # ========================================================================
    # return default func
    # ========================================================================
    return parser.parse_args(args)


def main(args=None):
    """The main routine."""
    if not args:
        # args are passed from command line (CLI)
        args = sys.argv[1:]
    args = parse_args(args)
    return args.process(args)


if __name__ == "__main__":
    main()
