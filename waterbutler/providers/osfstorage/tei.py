import io
import re
import logging

from bs4 import UnicodeDammit
from .migrator_tei import MigratorTEI
from .migrator_csv import MigratorCSV
from .migrator_tsv import MigratorTSV
from .xml_type_finder import XMLTypeFinder
from .file_type_finder import FileTypeFinder
from .entities_decoder import EntitiesDecoder
from .recognized_types import FileType, XMLType
from waterbutler.core.streams.base import BaseStream

logger = logging.getLogger(__name__)


class TeiHandler(BaseStream):
    """Stream-like handler that recognizes TEI/CSV files and migrate them to TEI P5."""

    def __init__(self, file_path, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__file_path = file_path
        self.__encoding = None
        self.text = io.StringIO()

        self.__text_binary = None
        self.__text_utf_8 = ""

        self.__file_type = FileType.OTHER
        self.__xml_type = XMLType.OTHER
        self.__prefixed = False

        self.__recognized = False
        self.__migrated = False
        self.__migrate = False
        self.__message = ""

        self.__is_tei_p5_unprefixed = False

    def recognize(self):
        self.__load_text_binary()

        try:
            recognize_results = UnicodeDammit(self.__text_binary)
            self.__encoding = recognize_results.original_encoding

            if not self.__encoding:
                raise Exception("Text encoding not recognized.")

        except Exception as ex:
            logger.info("Text encoding searching: {}".format(ex))

            return self.__migrate, self.__is_tei_p5_unprefixed

        else:
            self.__text_utf_8 = recognize_results.unicode_markup

            entities_decoder = EntitiesDecoder()
            text_utf_8_without_entities = entities_decoder.remove_non_xml_entities(self.__text_utf_8)
            text_binary_without_entities = text_utf_8_without_entities.encode(self.__encoding)

            file_type_finder = FileTypeFinder()
            self.__file_type = file_type_finder.check_if_xml(text_binary_without_entities)

            if self.__file_type == FileType.OTHER:
                self.__file_type = file_type_finder.check_if_csv_or_tsv(self.__text_utf_8)

            if self.__file_type == FileType.XML:
                self.__text_utf_8 = entities_decoder.decode_non_xml_entities(self.__text_utf_8)
                self.__text_utf_8 = self.__remove_encoding_declaration(self.__text_utf_8)

                xml_type_detector = XMLTypeFinder()
                self.__xml_type, self.__prefixed = xml_type_detector.find_xml_type(self.__text_utf_8)

            self.__text_utf_8 = self.__standardize_new_line_symbol(self.__text_utf_8)

            self.__migrate = self.__make_decision()
            self.__is_tei_p5_unprefixed = self.__check_if_tei_p5_unprefixed()
            self.__recognized = True

            return self.__migrate, self.__is_tei_p5_unprefixed

    def __load_text_binary(self):
        try:
            with open(self.__file_path, 'rb') as file:
                chunk = file.read()

                temp = io.BytesIO()

                while chunk:
                    temp.write(chunk)
                    chunk = file.read()

                self.__text_binary = temp.getvalue()

        except Exception as exc:
            self.error = exc
            return FileType.OTHER

    def __remove_encoding_declaration(self, text):
        first_line = text.splitlines()[0]

        regex = r'encoding=".*?"'
        match = re.search(regex, first_line)

        if match:
            encoding_declaration = match.group()

            text = text.replace(" " + encoding_declaration, '')
            text = text.replace(" ?>", "?>")

        return text

    def __standardize_new_line_symbol(self, text):
        text_standardized = text.replace('\r\n', '\n')

        return text_standardized

    def __make_decision(self):
        return self.__file_type in (FileType.CSV, FileType.TSV) or self.__file_type == FileType.XML and (
                self.__encoding != 'utf-8' or self.__prefixed or self.__xml_type == XMLType.TEI_P4)

    def __check_if_tei_p5_unprefixed(self):
        return self.__file_type == FileType.XML and self.__xml_type == XMLType.TEI_P5 and not self.__prefixed

    def migrate(self):
        if not self.__recognized:
            raise Exception("File recognition needed. Use \"recognize()\" method first.")

        elif not self.__migrate:
            raise Exception("No migration needed.")

        if self.__file_type == FileType.XML:
            migrator_tei = MigratorTEI()
            migrated_text = migrator_tei.migrate(self.__text_utf_8, self.__xml_type)
            self.text.write(migrated_text)

        elif self.__file_type == FileType.CSV:
            migrator_csv = MigratorCSV()
            migrated_text = migrator_csv.migrate(self.__text_utf_8)
            self.text.write(migrated_text)

        elif self.__file_type == FileType.TSV:
            migrator_tsv = MigratorTSV()
            migrated_text = migrator_tsv.migrate(self.__text_utf_8)
            self.text.write(migrated_text)

        self.text.seek(io.SEEK_SET)
        self.__prepare_message()
        self.__migrated = True

    def __prepare_message(self):
        prefixed = "prefixed " if self.__prefixed else ""

        file_type = {
            FileType.XML: "XML ",
            FileType.CSV: "CSV ",
            FileType.TSV: "TSV ",
            FileType.OTHER: "",
        }

        xml_type = {
            XMLType.TEI_P4: "TEI P4 ",
            XMLType.TEI_P5: "TEI P5 ",
            XMLType.OTHER: "",
        }

        message = ""

        if self.__file_type == FileType.XML and self.__xml_type == XMLType.TEI_P5 and not self.__prefixed:
            pass
        else:
            message += "Migrated file format from {0}{1}{2}to unprefixed TEI P5 XML.".format(prefixed,
                                                                                             xml_type[self.__xml_type],
                                                                                             file_type[
                                                                                                 self.__file_type])

        if self.__encoding != "utf-8":
            if message:
                message += " "

            message += "Changed file encoding from {0} to UTF-8.".format(self.__encoding)

        self.__message = message

    def get_message(self):
        return self.__message

    def close(self):
        self.text.close()

    async def read(self, size=-1):
        chunk = self.text.read(size)

        return bytes(chunk, "utf-8")

    async def _read(self, size):
        pass

    def size(self):
        pass

    def get_text(self):
        return self.text.getvalue()

    def is_migrated(self):
        return self.__migrated
