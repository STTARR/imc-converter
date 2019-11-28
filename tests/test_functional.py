"""Functional tests for reading and writing files."""

import os
import pickle
from pathlib import Path

import pytest
from imcconv import read_txt


def unpickle_ref(path):
    with open(path.with_suffix(".pickle"), "rb") as f:
        refarr = pickle.load(f)
    return refarr


def test_read_txt_valid(txt_valid_path):
    arr = read_txt(txt_valid_path)
    refarr = unpickle_ref(txt_valid_path)
    assert arr.equals(refarr)


def test_read_txt_raises_error_on_missing_values(
    txt_missing_intensity_values_path, txt_missing_xy_rows_path
):
    with pytest.raises(ValueError):
        read_txt(txt_missing_intensity_values_path)
        read_txt(txt_missing_xy_rows_path)


def test_read_txt_fill_missing_intensity_values(txt_missing_intensity_values_path):
    arr = read_txt(txt_missing_intensity_values_path, fill_missing=-1)
    refarr = unpickle_ref(txt_missing_intensity_values_path)
    assert arr.equals(refarr)


def test_read_txt_fill_missing_xy_rows(txt_missing_xy_rows_path):
    arr = read_txt(txt_missing_xy_rows_path, fill_missing=-1)
    refarr = unpickle_ref(txt_missing_xy_rows_path)
    assert arr.equals(refarr)
