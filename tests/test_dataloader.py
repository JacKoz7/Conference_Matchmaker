import pytest
from src.dataloader import load_from_file
import tempfile
import os


def test_load_from_file():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write("1\tattr1,attr2\tdesired1,desired2\n")
        temp_file.write("2\tattr3,attr4\tdesired3,desired4\n")
        temp_filename = temp_file.name

    try:
        result = load_from_file(temp_filename)

        expected = {
            1: {"attributes": ["attr1", "attr2"], "desired": ["desired1", "desired2"]},
            2: {"attributes": ["attr3", "attr4"], "desired": ["desired3", "desired4"]},
        }
        assert result == expected

    finally:
        # Clean up the temporary file
        os.unlink(temp_filename)


def test_load_from_file_empty():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_filename = temp_file.name

    try:
        result = load_from_file(temp_filename)
        assert result == {}

    finally:
        os.unlink(temp_filename)


def test_load_from_file_invalid_input():
    with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
        temp_file.write("invalid_data\n")
        temp_filename = temp_file.name

    try:
        with pytest.raises(ValueError):
            load_from_file(temp_filename)

    finally:
        os.unlink(temp_filename)
