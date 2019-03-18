from .corrector import AbstractCorrector
import re


class CorrectorDate(AbstractCorrector):
    def __init__(self):
        super().__init__()
        self._corrector_type = "date"

    def _get_declarations_to_switch(self, attribute_name, attribute_value):
        # TODO: clean this function with proper regular expressions
        if attribute_value == '""':
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            old_declaration = attribute_name + '="' + wrong_date + '"'
            new_declaration = attribute_name + '-custom="' + wrong_date + '"'

            return old_declaration, new_declaration

        elif "AM" in attribute_value or "B.C." in attribute_value or "BC" in attribute_value:
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            old_declaration = attribute_name + '="' + wrong_date + '"'
            new_declaration = attribute_name + '-custom="' + wrong_date + '"'

            return old_declaration, new_declaration

        elif attribute_value in ['"1.Aug-31.Oct"', '"157001-01"', '"-10"', '"03.01"']:
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            old_declaration = attribute_name + '="' + wrong_date + '"'
            new_declaration = attribute_name + '-custom="' + wrong_date + '"'

            return old_declaration, new_declaration

        elif re.match(r'"\d\d.\d\d"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            old_declaration = attribute_name + '="' + wrong_date + '"'
            new_declaration = attribute_name + '-custom="' + wrong_date + '"'

            return old_declaration, new_declaration

        elif re.match(r'"\d\d-\d\d-\d\d"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            old_declaration = attribute_name + '="' + wrong_date + '"'
            new_declaration = attribute_name + '-custom="' + wrong_date + '"'

            return old_declaration, new_declaration

        elif re.match(r'"\d\d\d\d-\d\d-\d\d/\d\d\d\d-\d\d-\d\d"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            old_declaration = attribute_name + '="' + wrong_date + '"'
            new_declaration = ('from="' + wrong_date[:10] + '" to="' + wrong_date[11:] + '" ' + attribute_name +
                               '-custom="' + wrong_date + '"')

            return old_declaration, new_declaration

        elif re.match(r'"[^0-9]+(\d\d\d-\d\d-\d\d)/(\d\d\d-\d\d-\d\d)"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            match = re.match(r'"[^0-9]+(\d\d\d-\d\d-\d\d)/(\d\d\d-\d\d-\d\d)"', attribute_value)

            old_declaration = attribute_name + '="' + wrong_date + '"'
            new_declaration = ('from="0' + match.group(1) + '" to="0' + match.group(2) + '" ' + attribute_name +
                               '-custom="' + wrong_date + '"')

            return old_declaration, new_declaration

        elif re.match(r'"(\d\d\d-\d\d-\d\d)/(\d\d)"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            match = re.match(r'"(\d\d\d-\d\d)-(\d\d)/(\d\d)"', attribute_value)

            old_declaration = attribute_name + '="' + wrong_date + '"'
            new_declaration = ('from="0' + match.group(1) + "-" + match.group(2) + '" to="0' + match.group(1) + "-" +
                               match.group(3) + '" ' + attribute_name + '-custom="' + wrong_date + '"')

            return old_declaration, new_declaration

        elif re.match(r'"(\d\d\d\d-\d\d)-(\d\d)/(\d\d)"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            match = re.match(r'"(\d\d\d\d-\d\d)-(\d\d)/(\d\d)"', attribute_value)

            old_declaration = attribute_name + '="' + wrong_date + '"'
            new_declaration = ('from="' + match.group(1) + "-" + match.group(2) + '" to="' + match.group(1) + "-" +
                               match.group(3) + '" ' + attribute_name + '-custom="' + wrong_date + '"')

            return old_declaration, new_declaration

        elif re.match(r'"\d"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            correct_date = "000" + wrong_date

        elif re.match(r'"\d\d"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            correct_date = "00" + wrong_date

        elif re.match(r'"\d\d[^0-9]+"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            correct_date = "00" + wrong_date[:2]

        elif re.match(r'"\d\d\d"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            correct_date = "0" + wrong_date

        elif re.match(r'"\d\d\d[^0-9]+"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            correct_date = "0" + wrong_date[:3]

        elif re.match(r'"[^0-9]+\d\d\d"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            correct_date = "0" + wrong_date[-3:]

        elif re.match(r'"\d\d\d\d[^0-9]+"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            correct_date = "0" + wrong_date[:4]

        elif re.match(r'"\d-\d\d"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            old_declaration = attribute_name + '="' + wrong_date + '"'
            new_declaration = attribute_name + '-custom="' + wrong_date + '"'

            return old_declaration, new_declaration

        elif re.match(r'"\d\d-\d\d"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            old_declaration = attribute_name + '="' + wrong_date + '"'
            new_declaration = attribute_name + '-custom="' + wrong_date + '"'

            return old_declaration, new_declaration

        elif re.match(r'"[^0-9]+\d\d-\d\d"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            old_declaration = attribute_name + '="' + wrong_date + '"'
            new_declaration = attribute_name + '-custom="' + wrong_date + '"'

            return old_declaration, new_declaration

        elif re.match(r'"[^0-9]+\d\d\d\d"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            correct_date = "0" + wrong_date[-4:]

        elif re.match(r'"\d\d\d-\d\d"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            correct_date = "0" + wrong_date

        elif re.match(r'"\d\d\d-\d\d-\d\d"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            correct_date = "0" + wrong_date

        elif re.match(r'"\d\d\d-\d\d-\d"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            correct_date = "0" + wrong_date[:7] + "0" + wrong_date[7:]

        elif re.match(r'"[^0-9]+\d\d\d-\d\d-\d\d"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            correct_date = "0" + wrong_date[-9:]

        elif re.match(r'"\d\d\d-\d-\d\d"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            correct_date = "0" + wrong_date[:4] + "0" + wrong_date[4:]

        elif re.match(r'"[^0-9]+(\d\d\d-\d\d-\d\d)[^0-9]+"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            match = re.match(r'"[^0-9]+(\d\d\d-\d\d-\d\d)[^0-9]+"', attribute_value)

            correct_date = "0" + match.group(1)

        elif re.match(r'"[^0-9]+\d\d\d\d-\d\d-\d\d"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            correct_date = wrong_date[-10:]

        elif re.match(r'"\d\d\d\d- \d\d"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            correct_date = wrong_date[:5] + wrong_date[6:]

        elif re.match(r'"\d\d\d\d-\d\d-\d\d[^0-9]+"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            correct_date = wrong_date[:10]

        elif re.match(r'"\d\d\d\d-\d\d- \d\d"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            correct_date = wrong_date[:8] + wrong_date[9:]

        elif re.match(r'"(\d\d)-(\d\d)-(\d\d\d\d)"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            match = re.match(r'"(\d\d)-(\d\d)-(\d\d\d\d)"', attribute_value)

            correct_date = match.group(3) + "-" + match.group(2) + "-" + match.group(1)

        elif re.match(r'"\d\d\d\d-\d-\d\d"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            correct_date = wrong_date[:5] + "0" + wrong_date[5:]

        elif re.match(r'"\d\d\d\d-\d\d-\d"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            correct_date = wrong_date[:8] + "0" + wrong_date[8:]

        elif re.match(r'"(\d\d\d\d-\d\d)-(\d\d\d)"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            match = re.match(r'"(\d\d\d\d-\d\d)-(\d\d\d)"', attribute_value)

            correct_date = "{}-{:2}".format(match.group(1), int(match.group(2)))

        elif re.match(r'"[^0-9]+(\d\d)-(\d\d)-(\d\d)"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            match = re.match(r'"[^0-9]+(\d\d)-(\d\d)-(\d\d)"', attribute_value)

            if int(match.group(3)) > 31:
                correct_date = "00" + match.group(match.group(4)) + "-" + match.group(3) + "-" + match.group(2)
            else:
                correct_date = "00" + wrong_date[-8:]

        elif re.match(r'"\d\d\d\d-\d"', attribute_value):
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            correct_date = wrong_date[:5] + "0" + wrong_date[5:]

        else:
            raise ValueError("Unknown {} format: {}. Add new instruction to 'CorrectorDate' class".format(
                self._corrector_type, attribute_value))

        old_declaration = attribute_name + '="' + wrong_date + '"'
        new_declaration = (attribute_name + '="' + correct_date + '"' + ' ' + attribute_name + '-custom="' +
                           wrong_date + '"')

        return old_declaration, new_declaration
