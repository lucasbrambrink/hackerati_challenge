import re

class FormatHelper(object):

    @staticmethod
    def pythonify(phrase):
        return re.sub(r'[!$%&\s-]', ' ', phrase.lower())