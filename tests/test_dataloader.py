import pytest
from src.dataloader import Dataloader
import tempfile
import os


@pytest.fixture  # konfiguracja danych wejściowych
def temp_file_factory():
    temp_files = []

    def create_temp_file(content=""):
        with tempfile.NamedTemporaryFile(mode="w", delete=False) as temp_file:
            temp_file.write(content)
            temp_files.append(temp_file.name)
        return temp_file.name

    # Kod przed yield jest wykonywany przed testem (setup)
    yield create_temp_file  # Wartość po yield jest przekazywana do testu.
    # Kod po yield jest wykonywany po zakończeniu testu (teardown)
    for file in temp_files:
        os.unlink(file)


@pytest.fixture
def sample_data():
    return "1\tattr1,attr2\tdesired1,desired2\n2\tattr3,attr4\tdesired3,desired4\n"


def test_load_from_file(temp_file_factory, sample_data):
    temp_filename = temp_file_factory(sample_data)
    data = Dataloader(temp_filename)
    result = data.load_from_file()

    expected = {
        1: {"attributes": ["attr1", "attr2"], "desired": ["desired1", "desired2"]},
        2: {"attributes": ["attr3", "attr4"], "desired": ["desired3", "desired4"]},
    }
    assert result == expected


def test_load_from_file_empty(temp_file_factory):
    temp_filename = temp_file_factory()
    data = Dataloader(temp_filename)
    result = data.load_from_file()
    assert result == {}


def test_load_from_file_invalid_input(temp_file_factory):
    temp_filename = temp_file_factory("invalid_data\n")
    data = Dataloader(temp_filename)
    with pytest.raises(ValueError):
        data.load_from_file()


def test_count_participants(temp_file_factory, sample_data):
    temp_filename = temp_file_factory(sample_data + "3\tattr5,attr6\tdesired5,desired6\n")
    data = Dataloader(temp_filename)
    result = data.count_participants()
    assert result == 3


def test_count_participants_empty(temp_file_factory):
    temp_filename = temp_file_factory()
    data = Dataloader(temp_filename)
    result = data.count_participants()
    assert result == 0


def test_count_participants_file_not_found():
    with pytest.raises(FileNotFoundError):
        data = Dataloader("non_existent_file.tsv")
        data.count_participants()
