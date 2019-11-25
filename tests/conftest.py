"""Global test configuration."""

import pytest
from pathlib import Path
import os

# Path(__file__).parent refers to the folder this test config is in
REFDIR = Path(__file__).parent / "reference_files"

def path_to_ref_file(fname: str):
    """Define path to file as a pytest fixture."""
    def get_path():
        path = REFDIR / fname
        assert path.exists() and path.is_file(), \
            f"Reference file {path} was not found or not a file."
        return path
    return pytest.fixture(get_path, scope="session")

txt_missing_intensity_values_path = path_to_ref_file("txt_missing_intensity_values.txt")
txt_missing_xy_rows_path = path_to_ref_file("txt_missing_xy_rows.txt")
txt_valid_path = path_to_ref_file("txt_valid.txt")