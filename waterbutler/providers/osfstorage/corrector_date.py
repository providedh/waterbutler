from .corrector import AbstractCorrector
import re


class CorrectorDate(AbstractCorrector):
    def __init__(self):
        super().__init__()
        self._corrector_type = "date"

    def _get_declarations_to_switch(self, attribute_name, attribute_value):
        if attribute_value == '""':
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            old_declaration = attribute_name + '="' + wrong_date + '"'
            new_declaration = attribute_name + '-custom="' + wrong_date + '"'

            return old_declaration, new_declaration

        elif re.match(r'"\d\d\d"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            correct_date = "0" + wrong_date[:3]

        elif re.match(r'"\d\d\d[^0-9]+"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            correct_date = "0" + wrong_date[:3]

        elif re.match(r'"[^0-9]+\d\d\d"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            correct_date = "0" + wrong_date[-3:]

        else:
            raise ValueError("Unknown {} format: {}. Add new instruction to 'CorrectorDate' class".format(
                self._corrector_type, attribute_value))

        old_declaration = attribute_name + '="' + wrong_date + '"'
        new_declaration = (attribute_name + '="' + correct_date + '"' + ' ' + attribute_name + '-custom="' +
                           wrong_date + '"')

        return old_declaration, new_declaration
