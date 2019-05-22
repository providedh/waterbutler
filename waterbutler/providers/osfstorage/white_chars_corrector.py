
CR_LF_CODES = ['&#xa;', '&#xd;', '&#10;', '&#13;']


class WhiteCharsCorrector:
    def __init__(self):
        pass

    def check_if_cr_lf_codes(self, text):
        for code in CR_LF_CODES:
            if code in text:
                return True

        return False

    def replace_cr_lf_codes(self, text):
        text_corrected = text
        for code in CR_LF_CODES:
            text_corrected = text_corrected.replace(code, '<lb/>')

        return text_corrected
