import os
import pytest

from waterbutler.providers.osfstorage.tei import TeiHandler

test_data_recognize__correct_file_uploaded = [
    "Py.1.xml",
    "Py.1.encoding.xml",
    "Py.1.encoding.windows-1250.xml",
    "Pn.1.xml",
    "Pn.2.xml",
    "T100014.without_html_entities.xml",
    "T100014.without_html_entities.prefixed.xml",
    "CREDITOR_short.TXT",
    "CREDITOR_T_short.TXT",
]


@pytest.mark.parametrize("input_file_name", test_data_recognize__correct_file_uploaded)
def test_recognize__correct_file_uploaded__true(input_file_name):
    dirname = os.path.dirname(__file__)
    file_path = os.path.join(dirname, "test_tei_example_files", "before_migration", input_file_name)

    tei_handler = TeiHandler(file_path)
    output = tei_handler.recognize()

    assert output is True


test_data_recognize__incorrect_text_file_uploaded = [
    "Py.1.corrupted.xml",
    "T100013.xml",
    "T100014.xml",
    "non_tei_xml_file.xml",
]


@pytest.mark.parametrize("input_file_name", test_data_recognize__incorrect_text_file_uploaded)
def test_recognize__incorrect_file_uplopaded__false(input_file_name):
    dirname = os.path.dirname(__file__)
    file_path = os.path.join(dirname, "test_tei_example_files", "before_migration", input_file_name)

    tei_handler = TeiHandler(file_path)
    output = tei_handler.recognize()

    assert output is False


test_data_recognize__non_text_file_uploaded = [
    "wrong_format.zip",
]


@pytest.mark.parametrize("input_file_name", test_data_recognize__non_text_file_uploaded)
def test_recognize__non_text_file_uploaded__exception(input_file_name):
    dirname = os.path.dirname(__file__)
    file_path = os.path.join(dirname, "test_tei_example_files", "before_migration", input_file_name)

    tei_handler = TeiHandler(file_path)
    output = tei_handler.recognize()

    assert output is False


test_data_recognize__unprefixed_tei_p5_file_uploaded = [
    "818114r122 - TEI Markup.xml",
    "Py.1.unprefixed.xml",
]


@pytest.mark.parametrize("input_file_name", test_data_recognize__unprefixed_tei_p5_file_uploaded)
def test_recognize__unprefixed_tei_p5_file_uplopaded__false(input_file_name):
    dirname = os.path.dirname(__file__)
    file_path = os.path.join(dirname, "test_tei_example_files", "before_migration", input_file_name)

    tei_handler = TeiHandler(file_path)
    output = tei_handler.recognize()

    assert output is False


test_data_migrate = [
    ("Py.1.xml", "Py.1.migrated.xml"),
    ("Py.1.encoding.xml", "Py.1.encoding.migrated.xml"),
    ("Py.1.encoding.windows-1250.xml", "Py.1.encoding.windows-1250.migrated.xml"),
    ("Pn.1.xml", "Pn.1.migrated.xml"),
    ("CREDITOR_short.TXT", "CREDITOR_short.migrated.xml"),
    ("CREDITOR_T_short.TXT", "CREDITOR_short.migrated.xml"),
]


@pytest.mark.parametrize("input_file_name, result_file_name", test_data_migrate)
def test_migrate__properly_recognized_file__migrated_string(input_file_name, result_file_name):
    dirname = os.path.dirname(__file__)
    input_file_path = os.path.join(dirname, "test_tei_example_files", "before_migration", input_file_name)

    tei_handler = TeiHandler(input_file_path)
    tei_handler.recognize()
    tei_handler.migrate()

    result = tei_handler.text.getvalue()

    result_file_path = os.path.join(dirname, "test_tei_example_files", "after_migration", result_file_name)

    with open(result_file_path, 'r') as file:
        expected = file.read()

    assert result == expected


def test_migrate__no_recognition_performed__exception():
    tei_handler = TeiHandler("some_name.txt")

    with pytest.raises(Exception) as ex:
        tei_handler.migrate()

    message = ex.value.args[0]

    assert message == "File recognition needed. Use recognize() method first."


test_data_migrate__no_migration_needed = [
    "Py.1.corrupted.xml",
    "T100013.xml",
    "818114r122 - TEI Markup.xml",
    "Py.1.unprefixed.xml",
]


@pytest.mark.parametrize("input_file_name", test_data_migrate__no_migration_needed)
def test_migrate__no_migration_needed__exception(input_file_name):
    dirname = os.path.dirname(__file__)
    input_file_path = os.path.join(dirname, "test_tei_example_files", "before_migration", input_file_name)

    tei_handler = TeiHandler(input_file_path)
    tei_handler.recognize()

    with pytest.raises(Exception) as ex:
        tei_handler.migrate()

    message = ex.value.args[0]

    assert message == "No migration needed."
