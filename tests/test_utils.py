"""Unit tests."""

import pytest
import os
from imcconv import imcconv
import numpy as np

def test_parse_channel_headers():
    assert imcconv._parse_channel_headers(["80ArAr(ArAr80Di)"])[0] == "ArAr(80)_80ArAr"