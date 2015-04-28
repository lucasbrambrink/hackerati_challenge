import re

class FormatHelper(object):

    @staticmethod
    def pythonify(phrase):
        return re.sub(r'[!$%&\s-]', ' ', phrase.lower())

    @staticmethod
    def capitalize(phrase):
        clean_phrase = "".join(char for char in phrase if char.isalpha() or char == " ").strip(' ')
        return " ".join(word[0].upper() + word[1:].lower() for word in clean_phrase.split(' '))