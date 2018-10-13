import configparser
import os


SERIES_CONFIGPARSE = {
    "Boruto": 'parent-dir',
    "Gintama": 'parent-dir',
    "Mahoutsukai no Yome": 'parent-dir',
    "One Piece": 'parent-dir',
    "American Dad": 'season',
    "Arrow": 'season',
    "Brooklyn Nine Nine": 'season',
    "Fresh off the Boat": 'season',
    "Homeland": 'season',
    "Lucifer": 'season',
    "Marvels Agents of S.H.I.E.L.D": 'season',
    "Supernatural": 'season',
    "The Big Bang Theory": 'season',
    "The Flash": 'season',
    "Vikings": 'season',
    "That 70s Show": 'season'
}


class TESTRuleBookEditor:
    def __init__(self, config_dir):
        self.config_dir = config_dir
        self.rule_book_path = os.path.join(self.config_dir + 'rule_book.ini')
        self.configparse = self.get_configpaser()

    def get_configpaser(self):
        configparse = configparser.ConfigParser(allow_no_value=True)
        configparse.read(self.rule_book_path)
        return configparse

    def save(self):
        with open(self.rule_book_path, 'w') as configfile:
            self.configparse.write(configfile)
