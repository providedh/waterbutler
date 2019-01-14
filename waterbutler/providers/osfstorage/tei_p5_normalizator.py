import re


class Tei5Normalizator():
    def __init__(self):
        pass

    def remove_default_tei5_namespace(self, text):
        """Function take a xml text and return xml text without default tei5 namespaces."""

        tei5_uri = "http://www.tei-c.org/ns/1.0"

        namespace_declaration = self.__find_declaration(text, tei5_uri)

        if namespace_declaration:
            tag_open, tag_close = self.__create_tags_to_clean(namespace_declaration)
            xml_content = self.__clean_tags(tag_open, tag_close, text)
            xml_content = self.__remove_declaration(namespace_declaration, xml_content)

            return xml_content
        else:
            raise Exception("No correct TEI P5 namespace declaration.")

    def __find_declaration(self, text, uri):
        regex = r'xmlns:.*?=' + '"' + uri + '"'
        match = re.search(regex, text)

        if match:
            namespace_declaration = match.group()

            return namespace_declaration

    def __create_tags_to_clean(self, namespace_declaration):
        declaration_without_xmlns = namespace_declaration.replace('xmlns:', '')

        prefix = declaration_without_xmlns.replace('="http://www.tei-c.org/ns/1.0"', '')

        tag_open = ''.join(('<', prefix, ':'))
        tag_close = ''.join(('</', prefix, ':'))

        return tag_open, tag_close

    def __clean_tags(self, tag_open, tag_close, text):
        text = text.replace(tag_open, '<')
        text = text.replace(tag_close, '</')

        return text

    def __remove_declaration(self, namespace_declaration, text):
        return text.replace(' ' + namespace_declaration, '')


if __name__ == '__main__':
    pass
