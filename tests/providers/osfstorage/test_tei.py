import os
import pytest

from waterbutler.providers.osfstorage.tei import TeiHandler

test_data_recognize__correct_file_uploaded = [
    "Py.1.xml",
    "Py.1.encoding.xml",
    "Py.1.encoding.windows-1250.xml",
    "Pn.1.xml",
    "Pn.2.xml",
    "T100013.xml",
    "T100014.xml",
    "T100015.xml",
    "T100016.xml",
    "T100017.xml",
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


test_data_recognize__missing_entity_in_dictionaries = [
    "T100014.missing.entity.xml",
]


@pytest.mark.parametrize("input_file_name", test_data_recognize__missing_entity_in_dictionaries)
def test_recognize__missing_entity_in_dictionaries__exception(input_file_name):
    dirname = os.path.dirname(__file__)
    input_file_path = os.path.join(dirname, "test_tei_example_files", "before_migration", input_file_name)

    tei_handler = TeiHandler(input_file_path)

    with pytest.raises(KeyError) as er:
        tei_handler.recognize()

    message = er.value.args[0]

    assert message == "Missing character \"fMedrun\" in \"custom_entities.py\" dictionary. " \
                      "Add this character to \"custom_entities.py\" dictionary"


test_data_migrate = [
    ("Py.1.xml", "Py.1.migrated.xml"),
    ("Py.1.encoding.xml", "Py.1.encoding.migrated.xml"),
    ("Py.1.encoding.windows-1250.xml", "Py.1.encoding.windows-1250.migrated.xml"),
    ("Pn.1.xml", "Pn.1.migrated.xml"),
    ("CREDITOR_short.TXT", "CREDITOR_short.migrated.xml"),
    ("CREDITOR_T_short.TXT", "CREDITOR_short.migrated.xml"),
    ("T100013.xml", "T100013.migrated.xml"),
    ("T100014.xml", "T100014.migrated.xml"),
    ("T100015.xml", "T100015.migrated.xml"),
    ("T100016.xml", "T100016.migrated.xml"),
    ("T100017.xml", "T100017.migrated.xml"),
    ("T100014.for.language.corrector.xml", "T100014.migrated.xml"),
    ("T100017.added.date.attributes.xml", "T100017.added.date.attributes.migrated.xml"),
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

    assert message == "File recognition needed. Use \"recognize()\" method first."


test_data_migrate__no_migration_needed = [
    "Py.1.corrupted.xml",
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


test_data_migrate__missing_instruction_for_date_correction = [
    "T100014.missing.instruction.for.date.correction.xml",
]


@pytest.mark.parametrize("input_file_name", test_data_migrate__missing_instruction_for_date_correction)
def test_migrate__missing_instruction_for_date_correction__exception(input_file_name):
    dirname = os.path.dirname(__file__)
    input_file_path = os.path.join(dirname, "test_tei_example_files", "before_migration", input_file_name)

    tei_handler = TeiHandler(input_file_path)

    tei_handler.recognize()

    with pytest.raises(ValueError) as er:
        tei_handler.migrate()

    message = er.value.args[0]

    assert message == "Unknown date format: \"38-01-01\". Add new instruction to 'CorrectorDate' class"


test_data_migrate__missing_instruction_for_language_correction = [
    "T100014.missing.instruction.for.language.correction.xml"
]


@pytest.mark.parametrize("input_file_name", test_data_migrate__missing_instruction_for_language_correction)
def test_migrate__missing_instruction_for_language_correction__exception(input_file_name):
    dirname = os.path.dirname(__file__)
    input_file_path = os.path.join(dirname, "test_tei_example_files", "before_migration", input_file_name)

    tei_handler = TeiHandler(input_file_path)

    tei_handler.recognize()

    with pytest.raises(ValueError) as er:
        tei_handler.migrate()

    message = er.value.args[0]

    assert message == "Unknown language format: \"asdfg\". Add new instruction to 'CorrectorLanguage' class"
