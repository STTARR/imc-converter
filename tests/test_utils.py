"""Unit tests."""

import pytest
import os
from imcconv.readers import _parse_txt_channel
import numpy as np


def test_parse_channel_headers():
    assert _parse_txt_channel("80ArAr(ArAr80Di)") == "ArAr(80)_80ArAr"