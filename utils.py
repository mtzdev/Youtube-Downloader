from PySide6.QtCore import QSettings
from os import path

class Settings:
    def __init__(self):
        self.settings = QSettings("YtDownloader-mtzdev", "Configurations")

    def setupSettings(self):
        self.settings.setValue('Default', '1.0')

        default_settings = {
            'Theme': 'dark',
            'SearchLimit': 12,
            'OutputPath': '',
            'language': 'pt-br'
        }
        for k, v in default_settings.items():
            if not self.settings.contains(k):
                self.settings.setValue(k, v)

    @property
    def theme(self):
        return self.settings.value('Theme', 'dark')

    @theme.setter
    def theme(self, theme: str):
        if theme.capitalize() in ['Claro', 'Escuro']:
            theme = 'light' if theme.capitalize() == 'Claro' else 'dark'

        if theme not in ['dark', 'light']:
            print('ERROR! Theme must be either "dark" or "light"')
            return

        self.settings.setValue('Theme', theme)

    @property
    def searchlimit(self):
        return int(self.settings.value('SearchLimit', 12))

    @searchlimit.setter
    def searchlimit(self, amount: int):
        try:
            amount = int(amount)
        except ValueError:
            print('ERROR! Search limit must be an integer')
            return

        if 4 <= amount <= 50:
            self.settings.setValue('SearchLimit', amount)
        else:
            print('ERROR! Search limit must be between 4 and 50')
            return

    @property
    def outputpath(self):
        path = self.settings.value('OutputPath', '')
        if path is None or path.strip() == '':
            return None
        return str(path)

    @outputpath.setter
    def outputpath(self, path: str):
        self.settings.setValue('OutputPath', path)

    @property
    def language(self):
        return self.settings.value('language', 'en')

    @language.setter
    def language(self, lang: str):
        self.settings.setValue('language', lang)


def get_resource(file):
    if "__compiled__" in globals():
        base_path = path.dirname(__file__)
    else:
        base_path = path.abspath(".")

    return path.join(base_path, file)