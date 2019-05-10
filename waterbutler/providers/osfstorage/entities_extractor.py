import json
from lxml import etree as et


class EntitiesExtractor:
    tags = ('person', 'place', 'org', 'event')
    namespaces = {'tei': 'http://www.tei-c.org/ns/1.0', 'xml': 'http://www.w3.org/XML/1998/namespace'}

    @classmethod
    def extract_entities_elements(cls, parsed_et):
        entites_elements = dict(
            (tag, parsed_et.xpath(".//tei:{}".format(tag), namespaces=cls.namespaces))
            for tag in ('place', 'org', 'event'))

        list_persons = parsed_et.findall(".//tei:listPerson", namespaces=cls.namespaces)
        list_persons = [listp for listp in list_persons if 'PROVIDEDH Annotators' not in listp.attrib.values()]
        text = parsed_et.find(".//tei:text", namespaces=cls.namespaces)
        persons = text.findall(".//tei:person", namespaces=cls.namespaces) if not list_persons else []

        for list_p in list_persons:
            persons.extend(list_p.findall(".//tei:person", namespaces=cls.namespaces))
        entites_elements['person'] = persons

        return entites_elements

    @classmethod
    def extract_entities(cls, contents):
        if not contents:
            return []
        parsed_et = et.fromstring(bytes(contents, 'UTF-8'))
        entites_elements = cls.extract_entities_elements(parsed_et)
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
            return element.attrib.get("{{{}}}id".format(cls.namespaces['xml']))

        id = getid(element)
        if id is None:
            subtags = cls.__list_subtags(element)
            if subtags:
                for tag in subtags:
                    id = getid(tag)
                    if id:
                        break

        return id if id is not None else ""

    @classmethod
    def __process_person_tags(cls, elements):
        def process_person_tag(element):
            id = cls.__extract_tag_id(element)
            text = element.text.strip() if element.text is not None else ""
            name = cls.__extract_subtag_text(element, 'name')
            forename = cls.__extract_subtag_text(element, 'forename')
            surname = cls.__extract_subtag_text(element, 'surname')

            name = name or text or "{} {}".format(forename, surname)
            return {'tag': 'person', 'id': id, 'name': name, 'forename': forename, 'surname': surname}

        return map(process_person_tag, elements)

    @staticmethod
    def __list_subtags(element):
        return element.findall(".//")

    @classmethod
    def __process_place_tags(cls, elements):
        def process_place_tag(element):
            id = cls.__extract_tag_id(element)
            subtags = ('placeName', 'placename', 'p', 'region', 'country')
            subtags_text = dict(zip(
                subtags,
                (cls.__extract_subtag_text(element, subtag) for subtag in subtags)
            ))
            return {'tag': 'place',
                    'id': id,
                    'name': subtags_text['placeName'] or subtags_text[
                        'placename'] or element.text.strip() if element.text is not None else "",
                    'desc': subtags_text['p'],
                    'region': subtags_text['region'],
                    'country': subtags_text['country']
                    }

        return map(process_place_tag, elements)

    @classmethod
    def __process_org_tags(cls, elements):
        def process_org_tag(element):
            id = cls.__extract_tag_id(element)
            name = cls.__extract_subtag_text(element, 'orgName')
            name = name or element.text.strip() if element.text is not None else ""
            return {'tag': 'place', 'id': id, 'name': name}

        return map(process_org_tag, elements)

    @classmethod
    def __process_event_tags(cls, elements):
        def process_event_tag(element):
            id = cls.__extract_tag_id(element)
            name = element.text.strip() if element.text is not None else ""
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
            entity['filepath'] = path
        return entites

    @staticmethod
    def to_json(entities):
        return json.dumps(entities, ensure_ascii=False)
