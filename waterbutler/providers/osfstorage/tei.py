import io
import re

from .entities_decoder import EntitiesDecoder
from .migrator_tei import MigratorTEI
from .migrator_csv import MigratorCSV
from .migrator_tsv import MigratorTSV
from .recognized_types import FileType, XMLType
from .xml_type_finder import XMLTypeFinder
from .encoding_finder import EncodingFinder
from .file_type_finder import FileTypeFinder
from waterbutler.core.streams.base import BaseStream


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
        self.__migrate = False
        self.__message = ""

    def recognize(self):
        self.__load_text_binary()

        try:
            encoding_finder = EncodingFinder()
            self.__encoding = encoding_finder.find_encoding(self.__text_binary)

        except Exception as ex:
            self.__message = ex

            return self.__migrate

        else:
            self.__text_utf_8 = self.__convert_to_utf_8(self.__text_binary, self.__encoding)

            entities_decoder = EntitiesDecoder()
            text_utf_8_without_entities = entities_decoder.remove_non_xml_entities(self.__text_utf_8)
            text_binary_without_entities = text_utf_8_without_entities.encode(self.__encoding)

            file_type_detector = FileTypeFinder()
            self.__file_type = file_type_detector.check_if_xml(text_binary_without_entities)

            if self.__file_type == FileType.OTHER:
                self.__file_type = file_type_detector.check_if_csv_or_tsv(self.__text_utf_8)

            if self.__file_type == FileType.XML:
                encoding_read_from_xml = encoding_finder.read_encoding_from_xml(self.__text_utf_8)

                if encoding_read_from_xml != self.__encoding:
                    self.__text_utf_8 = self.__convert_to_utf_8(self.__text_binary, encoding_read_from_xml)
                    self.__encoding = "utf-8"

                self.__text_utf_8 = entities_decoder.decode_non_xml_entities(self.__text_utf_8)
                self.__text_utf_8 = self.__remove_encoding_declaration(self.__text_utf_8)

                xml_type_detector = XMLTypeFinder()
                self.__xml_type, self.__prefixed = xml_type_detector.find_xml_type(self.__text_utf_8)

            self.__text_utf_8 = self.__standardize_new_line_symbol(self.__text_utf_8)

            self.__migrate = self.__make_decision()
            self.__recognized = True

            return self.__migrate

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

    def __convert_to_utf_8(self, binary, encoding):
        text_in_unicode = binary.decode(encoding)

        return text_in_unicode

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
        if (self.__file_type == FileType.XML and self.__xml_type == XMLType.TEI_P5 and
                self.__encoding != 'utf-8'):
            return True
        elif self.__file_type == FileType.XML and self.__xml_type == XMLType.TEI_P5 and self.__prefixed:
            return True
        elif self.__file_type == FileType.XML and self.__xml_type == XMLType.TEI_P4:
            return True
        elif self.__file_type == FileType.CSV:
            return True
        elif self.__file_type == FileType.TSV:
            return True
        else:
            return False

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

    def __prepare_message(self):
        message = "Successful migration."

        self.__message = message

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
