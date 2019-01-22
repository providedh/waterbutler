import chardet
import re


class EncodingFinder:
    def __init__(self):
        pass

    def find_encoding(self, text_binary):
        result = chardet.detect(text_binary)
        encoding = result['encoding']

        if encoding is None:
            raise Exception("Encoding not detected.")

        return encoding

    def read_encoding_from_xml(self, text):
        first_line = text.splitlines()[0]

        regex = r'encoding=".*?"'
        match = re.search(regex, first_line)

        if match:
            declaration_of_encoding = match.group()
            encoding = declaration_of_encoding.replace('encoding=', '')
            encoding = encoding.replace('"', '')

            return encoding.lower()

        else:
            return "utf-8"
