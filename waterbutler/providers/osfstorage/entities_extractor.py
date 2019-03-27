import json
from lxml import etree as et


class EntitiesExtractor:
    tags = ('person', 'place', 'org', 'event')
    namespaces = {'tei': 'http://www.tei-c.org/ns/1.0'}

    @classmethod
    def __extract_entities_elements(cls, contents):
        parsed = et.fromstring(bytes(contents, 'UTF-8'))
        text = parsed.find("tei:text", namespaces=cls.namespaces)
        if text is None: return []

        entites_elements = dict(
            (tag, text.xpath(".//tei:{}".format(tag), namespaces=cls.namespaces))
            for tag in cls.tags)

        return entites_elements

    @classmethod
    def extract_entities(cls, contents):
        entites_elements = cls.__extract_entities_elements(contents)
        result = []
        for tag, elements in entites_elements.items():
            result.extend(cls.__process_tags(tag, elements))

        return result

    @classmethod
    def __extract_subtag_text(cls, element, subtag):
        elem = element.find(".//tei:{}".format(subtag), namespaces=cls.namespaces)
        return elem.text.strip() if elem is not None and elem.text is not None else ""

    @classmethod
    def __extract_tag_id(cls, element):
        def getid(element):
            return [element.attrib[i].strip() for i in element.attrib if i[-2:] == 'id']

        id = getid(element)
        if not id:
            subtags = cls.__list_subtags(element)
            if subtags:
                for tag in subtags:
                    id = getid(tag)
                    if id: break

        return id[0] if id else ""

    @classmethod
    def __process_person_tags(cls, elements):
        def process_person_tag(element):
            id = cls.__extract_tag_id(element)
            name = cls.__extract_subtag_text(element, 'name')
            forename = cls.__extract_subtag_text(element, 'forename')
            surname = cls.__extract_subtag_text(element, 'surname')

            name = name or "{} {}".format(forename, surname)
            return {'tag': 'person', 'id': id, 'name': name, 'forename': forename, 'surname': surname}

        return map(process_person_tag, elements)

    @staticmethod
    def __list_subtags(element):
        return element.findall(".//")

    @classmethod
    def __process_place_tags(cls, elements):
        def process_place_tag(element):
            id = cls.__extract_tag_id(element)
            name = cls.__extract_subtag_text(element, 'placeName')
            name = name or element.text.strip()
            return {'tag': 'place', 'id': id, 'name': name}

        return map(process_place_tag, elements)

    @classmethod
    def __process_org_tags(cls, elements):
        def process_org_tag(element):
            id = cls.__extract_tag_id(element)
            name = cls.__extract_subtag_text(element, 'orgName')
            name = name or element.text.strip()
            return {'tag': 'place', 'id': id, 'name': name}

        return map(process_org_tag, elements)

    @classmethod
    def __process_event_tags(cls, elements):
        def process_event_tag(element):
            id = cls.__extract_tag_id(element)
            name = element.text.strip()
            return {'tag': 'place', 'id': id, 'name': name}

        return map(process_event_tag, elements)

    @classmethod
    def __process_tags(cls, tag, elements):
        functions = (cls.__process_person_tags,
                     cls.__process_place_tags,
                     cls.__process_org_tags,
                     cls.__process_event_tags)

        return dict(zip(cls.tags, functions))[tag](elements)

    @staticmethod
    def extend_entities(entites, project, path):
        for entity in entites:
            entity['project'] = project
            entity['path'] = path
        return entites

    @staticmethod
    def encode_entities(entities):
        return json.dumps(entities)
