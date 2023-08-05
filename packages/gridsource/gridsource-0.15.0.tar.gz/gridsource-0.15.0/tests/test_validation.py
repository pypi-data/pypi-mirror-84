#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""Tests for `gridsource` package."""

import os
import shutil
from pprint import pprint as pp

import numpy as np
import pandas as pd
import pytest

from gridsource import Data as IVData
from gridsource import ValidData as VData
from gridsource.validation import DataFrameSchematizer


def test_DFS_00_schema_bulding():
    """test DataFrameSchematizer class.
    DataFrameSchematizer class is purely internal and wrapped by VData or IVData
    """
    v = DataFrameSchematizer()
    columns_specs = """\
---
id:
  types: integer
  unique: true
  mandatory: true
name:
  types: string
  mandatory: true
firstname:
  types: string
age:
  types: integer
  minimum: 0
life_nb:
  types: integer
  mandatory: true
  maximum: 4
"""
    v.add_columns(columns_specs)
    # build valid jsonschema
    schema = v.build()
    expected_schema = {
        "$schema": "http://json-schema.org/draft-07/schema#",
        "type": "object",
        "properties": {
            "id": {"type": "array", "items": {"type": "integer"}, "uniqueItems": True},
            "name": {
                "type": "array",
                "items": {"type": "string"},
                "uniqueItems": False,
            },
            "firstname": {
                "type": "array",
                "items": {"anyOf": [{"type": "string"}, {"type": "null"}]},
                "uniqueItems": False,
            },
            "age": {
                "type": "array",
                "items": {
                    "anyOf": [{"type": "integer"}, {"type": "null"}],
                    "minimum": 0,
                },
                "uniqueItems": False,
            },
            "life_nb": {
                "type": "array",
                "items": {"type": "integer", "maximum": 4},
                "uniqueItems": False,
            },
        },
    }
    assert schema == expected_schema


def test_DFS_01_validation():
    """test DataFrameSchematizer class validation.
    DataFrameSchematizer class is purely internal and wrapped by VData or IVData
    """
    v = DataFrameSchematizer()
    columns_specs = """\
---
id:
  types: integer
  unique: true
  mandatory: true
name:
  types: string
  mandatory: true
firstname:
  types: string
age:
  types: integer
  minimum: 0
life_nb:
  types: integer
  mandatory: true
  maximum: 4
"""
    v.add_columns(columns_specs)
    df = df = pd.DataFrame(
        {
            "id": {7: 0, 1: 1, 2: 5},
            "name": {7: "Doe", 1: "Fante", 2: "Mercury"},
            "firstname": {7: "John", 2: "Freddy", 1: "Richard"},
            "age": {7: "42", 1: 22},
            "life_nb": {7: 5, 1: "hg", 2: 15},
        }
    )
    is_valid, errors = v.validate(df)
    assert is_valid is False
    expected_errors = {
        ("age", 0): [
            "'42' is not valid under any of the given schemas",
            "'42' is not of type 'integer'",
            "'42' is not of type 'null'",
        ],
        ("life_nb", 0): ["5 is greater than the maximum of 4"],
        ("life_nb", 1): ["'hg' is not of type 'integer'"],
        ("life_nb", 2): ["15 is greater than the maximum of 4"],
    }
    assert errors == expected_errors


def test_VData_00():
    data = VData()
    # ------------------------------------------------------------------------
    # Create a schema for "test" tab
    # This example show a YAML schema syntax,
    # but json or plain dict is also OK:
    from io import StringIO

    data.set_schema(
        "test",
        "---"
        "\nid:"
        "\n  types: integer"
        "\n  unique: true"
        "\n  mandatory: true"
        "\nname:"
        "\n  types: string"
        "\n  mandatory: true"
        "\nfirstname:"
        "\n  types: string"
        "\nage:"
        "\n  types: integer"
        "\n  minimum: 0"
        "\nlife_nb:"
        "\n  types: integer"
        "\n  mandatory: true"
        "\n  maximum: 4",
    )
    # ------------------------------------------------------------------------
    # create dummy data
    data._data["test"] = pd.DataFrame(
        {
            "id": {7: 0, 1: 1, 2: 5},
            "name": {7: "Doe", 1: "Fante", 2: "Mercury"},
            "firstname": {7: "John", 2: "Freddy", 1: "Richard"},
            "age": {7: "42", 1: 22},
            "life_nb": {7: 5, 1: "hg", 2: 15},
        }
    )
    expected_report = {
        ("age", 0): [
            "'42' is not valid under any of the given schemas",
            "'42' is not of type 'integer'",
            "'42' is not of type 'null'",
        ],
        ("life_nb", 0): ["5 is greater than the maximum of 4"],
        ("life_nb", 1): ["'hg' is not of type 'integer'"],
        ("life_nb", 2): ["15 is greater than the maximum of 4"],
    }
    is_valid, errors = data.validate_tab("test")
    assert is_valid is False
    assert errors == expected_report


# =============================================================================
# level 1 : read files on disk
# =============================================================================


@pytest.fixture
def datadir():
    """
    Basic IO Structure
    """
    test_dir = os.path.dirname(os.path.realpath(__file__))
    indir = os.path.join(test_dir, "data")
    outdir = os.path.join(test_dir, "_out")
    # ensure outdir exists and is empty
    if os.path.isdir(outdir):
        shutil.rmtree(outdir)
    os.makedirs(outdir)
    return indir, outdir


def test_IVData_00(datadir):
    indir, outdir = datadir
    data = IVData()
    data.read_excel(os.path.join(indir, "test_00.xlsx"))
    data.read_schema(os.path.join(indir, "test_00.schema.yaml"))
    for tab in ("names", "cars", "empty"):
        print('checking "%s"' % tab, end="... ")
        is_ok, errors = data.validate_tab(tab)
        try:
            assert is_ok is True
        except:
            print("OUPS!")
            __import__("pdb").set_trace()
        else:
            print("OK")
        assert errors == {}
    # ------------------------------------------------------------------------
    # export and reimport to/from various formats
    for extension in (".cfg", ".xlsx", ".ini"):
        target = os.path.join(outdir, "test_00" + extension)
        print("test '%s' extension" % target)
        assert not os.path.isfile(target)
        data.to(target)
        assert os.path.isfile(target)
        # --------------------------------------------------------------------
        # read the newly created file
        data_new = IVData()
        data_new.read(target)
        data_new.read_schema(os.path.join(indir, "test_00.schema.yaml"))
        for tab in data._data.keys():
            print('checking "%s"' % tab, end="... ")
            is_ok, errors = data_new.validate_tab(tab)
            try:
                assert is_ok is True
            except:
                print("OUPS!")
                __import__("pdb").set_trace()
            else:
                print("OK")
            assert errors == {}


def test_IVData_01(datadir):
    indir, outdir = datadir
    data = IVData()
    data.read_excel(os.path.join(indir, "test_00.xlsx"))
    data.read_schema(os.path.join(indir, "test_00.schema.yaml"))
    ret = data.validate()
    assert len(ret) == 0


def test_IVData_02(datadir):
    indir, outdir = datadir
    data = IVData()
    data.read_excel(os.path.join(indir, "test_00.xlsx"))
    data.read_schema(os.path.join(indir, "test_00.schema2.yaml"))
    ret = data.validate()
    assert ret == {"cars": {("Year", 2): ["None is not of type 'integer'"]}}


def test_IVData_03(datadir):
    """ make schema a bit more complex """
    indir, outdir = datadir
    data = IVData()
    data.read_excel(os.path.join(indir, "test_01.xlsx"))
    data.read_schema(os.path.join(indir, "test_01.schema2.yaml"))
    ret = data.validate()
    assert len(ret) == 0


def test_IVData_04(datadir):
    """ make schema a bit more complex: add generic keys """
    indir, outdir = datadir
    data = IVData()
    data.read_excel(os.path.join(indir, "test_02.xlsx"))
    data.read_schema(os.path.join(indir, "test_02.schema.yaml"), debug=True)
    ret = data.validate()
    assert len(ret) == 1
    expected_errors = {
        "french_cars": {
            ("brand", 2): [
                "'Citroën' is not one of ['Peugeot', 'Toyota', 'Ford', 'Renault']"
            ]
        }
    }
    assert ret == expected_errors
