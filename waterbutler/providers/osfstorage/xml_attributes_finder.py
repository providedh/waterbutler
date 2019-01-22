import re

from io import BytesIO
from lxml import etree


class XMLAttributesFinder:
    def __init__(self):
        self.text_binary = None
        self.text_utf_8 = ""

        self.tree = None

    def find_xml_attributes(self, text):
        self.text_utf_8 = text
        self.text_binary = self.text_utf_8.encode('utf-8')

        self.tree = etree.parse(BytesIO(self.text_binary))

        root_tag = self.__get_root_tag(self.tree)
        prefix = self.__get_prefix()
        tei_p5_ns_schema = self.__is_tei_p5_ns_schema()

        return root_tag, prefix, tei_p5_ns_schema

    def __get_root_tag(self, parsed_xml_tree):
        root = parsed_xml_tree.getroot()

        root_tag_with_prefix = root.tag

        root_tag = self.__remove_prefix_from_root_tag(root_tag_with_prefix)

        return root_tag

    def __remove_prefix_from_root_tag(self, root_tag_with_prefix):
        regex = r'\{.*?\}'
        match = re.search(regex, root_tag_with_prefix)
        if match:
            prefix_to_remove = match.group()

            root_tag = root_tag_with_prefix.replace(prefix_to_remove, '')

            return root_tag

        else:
            root_tag = root_tag_with_prefix

            return root_tag

    def __get_prefix(self):
        regex = r'<.*?:TEI'
        match = re.search(regex, self.text_utf_8)
        if match:
            prefix = match.group()

            prefix = prefix.replace(':TEI', '')
            prefix = prefix.replace('<', '')

            return prefix

    def __is_tei_p5_ns_schema(self):
        regex = r'xmlns:.*?="http://www.tei-c.org/ns/1.0"'
        match = re.search(regex, self.text_utf_8)
        if match:
            return True
        else:
            return False
