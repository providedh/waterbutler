import re

from .encoding_finder import EncodingFinder
from .xml_attributes_finder import XMLAttributesFinder
from .recognized_types import XMLType


class MigratorTEI:
    def __init__(self):
        self.__text = ""
        self.__prefix = ""
        self.__xml_type = XMLType.OTHER

    def migrate(self, text, xml_type):
        self.__text = text
        self.__xml_type = xml_type

        encoding_finder = EncodingFinder()
        encoding_read_from_xml = encoding_finder.read_encoding_from_xml(self.__text)

        if encoding_read_from_xml != 'utf-8':
            self.__text = self.__encoding_declaration_update(self.__text)

        xml_attributes_finder = XMLAttributesFinder()
        _, self.__prefix, _ = xml_attributes_finder.find_xml_attributes(self.__text)

        if self.__prefix:
            self.__text = self.__tags_update(self.__text)
            self.__text = self.__namespace_declaration_update(self.__text)

        if self.__xml_type == XMLType.TEI_P4:
            pass

        return self.__text

    def __encoding_declaration_update(self, text):
        first_line = text.splitlines()[0]

        regex = r'encoding=".*?"'
        match = re.search(regex, first_line)

        if match:
            old_encoding_declaration = match.group()
            new_encoding_declaration = 'encoding="UTF-8"'

            text = text.replace(old_encoding_declaration, new_encoding_declaration)
            return text

    def __tags_update(self, text):
        old_tag_open = ''.join(('<', self.__prefix, ':'))
        old_tag_close = ''.join(('</', self.__prefix, ':'))

        new_tag_open = '<'
        new_tag_close = '</'

        text = text.replace(old_tag_open, new_tag_open)
        text = text.replace(old_tag_close, new_tag_close)

        return text

    def __namespace_declaration_update(self, text):
        old_namespace_declaration = 'xmlns:' + self.__prefix + '='
        new_namespace_declaration = 'xmlns='

        text = text.replace(old_namespace_declaration, new_namespace_declaration)

        return text
