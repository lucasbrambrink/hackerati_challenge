import re
import random

class FormatHelper(object):

    @staticmethod
    def pythonify(phrase):
        return re.sub(r'[!$%&\s-]', ' ', phrase.lower())

    @staticmethod
    def capitalize(phrase):
        clean_phrase = "".join(char for char in phrase if char.isalpha() or char == " ").strip(' ')
        return " ".join(word[0].upper() + word[1:].lower() for word in clean_phrase.split(' ') if len(word) > 1)

    @staticmethod
    def name_to_username(name):
        username = "_".join(word.lower() for word in name.split())
        num = str(random.randint(0, 9)) + str(random.randint(0, 9))
        return "{username}{num}".format(
            username=username,
            num=num
        )

    @staticmethod
    def format_money(num):
        return "${0:.2f}".format(float(num))