from .corrector import AbstractCorrector
import re


class CorrectorDate(AbstractCorrector):
    def __init__(self):
        super().__init__()
        self._corrector_type = "date"

    def _get_declarations_to_switch(self, attribute_name, attribute_value):
        attribute_value_without_space = attribute_value.replace(' ', '')

        # TODO: refactor
        if "AM" in attribute_value or "B.C." in attribute_value or "BC" in attribute_value:
            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            old_declaration = attribute_name + '="' + wrong_date + '"'
            new_declaration = attribute_name + '-custom="' + wrong_date + '"'

            return old_declaration, new_declaration

        # "aaa1234-1234-1234/1234-1234-1234bbb"
        elif re.match(r'"\D*?([\d]{1,4})-([\d]{1,4})-([\d]{1,4})/([\d]{1,4})-([\d]{1,4})-([\d]{1,4})\D*?"',
                      attribute_value_without_space):
            match = re.match(r'"\D*?([\d]{1,4})-([\d]{1,4})-([\d]{1,4})/([\d]{1,4})-([\d]{1,4})-([\d]{1,4})\D*?"',
                             attribute_value_without_space)

            values_1 = [
                int(match.group(1)),
                int(match.group(2)),
                int(match.group(3))
            ]

            year_candidate_1 = []
            month_candidate_1 = []
            day_candidate_1 = []

            for value in values_1:
                if value > 31:
                    year_candidate_1.append(value)
                elif value > 12:
                    day_candidate_1.append(value)
                else:
                    month_candidate_1.append(value)

            values_2 = [
                int(match.group(4)),
                int(match.group(5)),
                int(match.group(6))
            ]

            year_candidate_2 = []
            month_candidate_2 = []
            day_candidate_2 = []

            for value in values_2:
                if value > 31:
                    year_candidate_2.append(value)
                elif value > 12:
                    day_candidate_2.append(value)
                else:
                    month_candidate_2.append(value)

            if (len(year_candidate_1) == len(month_candidate_1) == len(day_candidate_1) ==
                    len(year_candidate_2) == len(month_candidate_2) == len(day_candidate_2) == 1):
                wrong_date = attribute_value
                wrong_date = wrong_date.replace('"', '')

                old_declaration = attribute_name + '="' + wrong_date + '"'

                new_declaration = 'from="{:04d}-{:02d}-{:02d}" to="{:04d}-{:02d}-{:02d}" {}-custom="{}"'.format(
                    year_candidate_1[0], month_candidate_1[0], day_candidate_1[0], year_candidate_2[0],
                    month_candidate_2[0], day_candidate_2[0], attribute_name, wrong_date)

                return old_declaration, new_declaration

            else:
                wrong_date = attribute_value
                wrong_date = wrong_date.replace('"', '')

                old_declaration = attribute_name + '="' + wrong_date + '"'
                new_declaration = attribute_name + '-custom="' + wrong_date + '"'

                return old_declaration, new_declaration

        # "aaa1234-1234-1234/1234-1234bbb"
        elif re.match(r'"\D*?([\d]{1,4})-([\d]{1,4})-([\d]{1,4})/([\d]{1,4})-([\d]{1,4})\D*?"',
                      attribute_value_without_space):
            match = re.match(r'"\D*?([\d]{1,4})-([\d]{1,4})-([\d]{1,4})/([\d]{1,4})-([\d]{1,4})\D*?"',
                             attribute_value_without_space)

            values_1 = [
                int(match.group(1)),
                int(match.group(2)),
                int(match.group(3))
            ]

            year_candidate_1 = []
            month_candidate_1 = []
            day_candidate_1 = []

            for value in values_1:
                if value > 31:
                    year_candidate_1.append(value)
                elif value > 12:
                    day_candidate_1.append(value)
                else:
                    month_candidate_1.append(value)

            values_2 = [
                int(match.group(4)),
                int(match.group(5))
            ]

            year_candidate_2 = []
            month_candidate_2 = []
            day_candidate_2 = []

            for value in values_2:
                if value > 31:
                    year_candidate_2.append(value)
                elif value > 12:
                    day_candidate_2.append(value)
                else:
                    month_candidate_2.append(value)

            if (len(year_candidate_1) == len(month_candidate_1) == len(day_candidate_1) ==
                    len(month_candidate_2) == len(day_candidate_2) == 1):
                wrong_date = attribute_value
                wrong_date = wrong_date.replace('"', '')

                old_declaration = attribute_name + '="' + wrong_date + '"'

                new_declaration = 'from="{0:04d}-{1:02d}-{2:02d}" to="{0:04d}-{3:02d}-{4:02d}" {5}-custom="{6}"'.format(
                    year_candidate_1[0], month_candidate_1[0], day_candidate_1[0], month_candidate_2[0],
                    day_candidate_2[0], attribute_name, wrong_date)

                return old_declaration, new_declaration

            else:
                wrong_date = attribute_value
                wrong_date = wrong_date.replace('"', '')

                old_declaration = attribute_name + '="' + wrong_date + '"'
                new_declaration = attribute_name + '-custom="' + wrong_date + '"'

                return old_declaration, new_declaration

        # "aaa1234-1234-1234/1234bbb"
        elif re.match(r'"\D*?([\d]{1,4})-([\d]{1,4})-([\d]{1,4})/([\d]{1,4})\D*?"',
                      attribute_value_without_space):
            match = re.match(r'"\D*?([\d]{1,4})-([\d]{1,4})-([\d]{1,4})/([\d]{1,4})\D*?"',
                             attribute_value_without_space)

            values_1 = [
                int(match.group(1)),
                int(match.group(2)),
                int(match.group(3))
            ]

            year_candidate_1 = []
            month_candidate_1 = []
            day_candidate_1 = []

            for value in values_1:
                if value > 31:
                    year_candidate_1.append(value)
                elif value > 12:
                    day_candidate_1.append(value)
                else:
                    month_candidate_1.append(value)

            values_2 = [
                int(match.group(4)),
            ]

            year_candidate_2 = []
            month_candidate_2 = []
            day_candidate_2 = []

            for value in values_2:
                if value > 31:
                    year_candidate_2.append(value)
                elif value > 12:
                    day_candidate_2.append(value)
                else:
                    month_candidate_2.append(value)

            if len(year_candidate_1) == len(month_candidate_1) == len(day_candidate_1) == len(day_candidate_2) == 1:
                wrong_date = attribute_value
                wrong_date = wrong_date.replace('"', '')

                old_declaration = attribute_name + '="' + wrong_date + '"'

                new_declaration = 'from="{0:04d}-{1:02d}-{2:02d}" to="{0:04d}-{1:02d}-{3:02d}" {4}-custom="{5}"'.format(
                    year_candidate_1[0], month_candidate_1[0], day_candidate_1[0], day_candidate_2[0],
                    attribute_name, wrong_date)

                return old_declaration, new_declaration

            else:
                wrong_date = attribute_value
                wrong_date = wrong_date.replace('"', '')

                old_declaration = attribute_name + '="' + wrong_date + '"'
                new_declaration = attribute_name + '-custom="' + wrong_date + '"'

                return old_declaration, new_declaration

        # "aaa1234-1234-1234bbb"
        elif re.match(r'"\D*?([\d]{1,4})-([\d]{1,4})-([\d]{1,4})\D*?"', attribute_value_without_space):
            match = re.match(r'"\D*?([\d]{1,4})-([\d]{1,4})-([\d]{1,4})\D*?"', attribute_value_without_space)

            values = [
                int(match.group(1)),
                int(match.group(2)),
                int(match.group(3))
            ]

            year_candidate = []
            month_candidate = []
            day_candidate = []

            for value in values:
                if value > 31:
                    year_candidate.append(value)
                elif value > 12:
                    day_candidate.append(value)
                else:
                    month_candidate.append(value)

            if len(year_candidate) == len(month_candidate) == len(day_candidate) == 1:
                wrong_date = attribute_value
                wrong_date = wrong_date.replace('"', '')

                correct_date = "{:04d}-{:02d}-{:02d}".format(year_candidate[0], month_candidate[0], day_candidate[0])

            else:
                wrong_date = attribute_value
                wrong_date = wrong_date.replace('"', '')

                old_declaration = attribute_name + '="' + wrong_date + '"'
                new_declaration = attribute_name + '-custom="' + wrong_date + '"'

                return old_declaration, new_declaration

        # "aaa1234-1234bbbb"
        elif re.match(r'"\D*?([\d]{1,4})-([\d]{1,4})\D*?"', attribute_value_without_space):
            match = re.match(r'"\D*?([\d]{1,4})-([\d]{1,4})\D*?"', attribute_value_without_space)

            values = [
                int(match.group(1)),
                int(match.group(2)),
            ]

            year_candidate = []
            month_candidate = []
            day_candidate = []

            for value in values:
                if value > 31:
                    year_candidate.append(value)
                elif value > 12:
                    day_candidate.append(value)
                else:
                    month_candidate.append(value)

            if len(year_candidate) == len(month_candidate) == 1:
                wrong_date = attribute_value
                wrong_date = wrong_date.replace('"', '')

                correct_date = "{:04d}-{:02d}".format(year_candidate[0], month_candidate[0])

            else:
                wrong_date = attribute_value
                wrong_date = wrong_date.replace('"', '')

                old_declaration = attribute_name + '="' + wrong_date + '"'
                new_declaration = attribute_name + '-custom="' + wrong_date + '"'

                return old_declaration, new_declaration

        # "aaa1234bbb"
        elif re.match(r'"\D*?([\d]{1,4})\D*?"', attribute_value_without_space):
            match = re.match(r'"\D*?([\d]{1,4})\D*?"', attribute_value_without_space)

            values = [
                int(match.group(1)),
            ]

            year_candidate = []
            month_candidate = []
            day_candidate = []

            for value in values:
                if value > 31:
                    year_candidate.append(value)
                elif value > 12:
                    day_candidate.append(value)
                else:
                    month_candidate.append(value)

            if len(year_candidate) == 1:
                wrong_date = attribute_value
                wrong_date = wrong_date.replace('"', '')

                correct_date = "{:04d}".format(year_candidate[0])

            else:
                wrong_date = attribute_value
                wrong_date = wrong_date.replace('"', '')

                old_declaration = attribute_name + '="' + wrong_date + '"'
                new_declaration = attribute_name + '-custom="' + wrong_date + '"'

                return old_declaration, new_declaration

        else:
            # raise ValueError("Unknown {} format: {}. Add new instruction to 'CorrectorDate' class".format(
            #     self._corrector_type, attribute_value))

            wrong_date = attribute_value
            wrong_date = wrong_date.replace('"', '')

            old_declaration = attribute_name + '="' + wrong_date + '"'
            new_declaration = attribute_name + '-custom="' + wrong_date + '"'

            return old_declaration, new_declaration

        old_declaration = attribute_name + '="' + wrong_date + '"'
        new_declaration = (attribute_name + '="' + correct_date + '"' + ' ' + attribute_name + '-custom="' +
                           wrong_date + '"')

        return old_declaration, new_declaration
