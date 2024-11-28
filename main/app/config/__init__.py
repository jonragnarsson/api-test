from os.path import join, dirname
from pathlib import Path
from typing import List
from dotenv import dotenv_values


class Config:
    ROOT_URL: str = ''
    BASE_DIR: str = ''
    AVAILABLE_SYMBOLS: List = []
    FIXER_KEY: str = ''
    URL_WITH_KEY: str = ''
    
    def update_env(self):
        self.BASE_DIR = dirname(Path(__file__).resolve().parent.parent)
        envpath = join(self.BASE_DIR, '.env')
        self.__dict__.update(**dotenv_values(envpath))
        self.URL_WITH_KEY = f'{self.ROOT_URL}?access_key={self.FIXER_KEY}'

        
class Development(Config):
    def __init__(self):
        self.ROOT_URL = 'https://data.fixer.io/api/latest'
        self.AVAILABLE_SYMBOLS = ['GBP', 'DKK', 'SWE', 'ISK', 'NOK', 'USD', 'CHF', 'EUR', 'BRL', 'CAD', 'CNY', 'JPY']
        self.update_env()


class Production(Config):
    pass
    
class Test(Development):
    pass


def env() -> Config:
    basedir = dirname(Path(__file__).resolve().parent)
    envpath = join(basedir, '.env')
    values = dotenv_values(envpath)
    env = values.get('ENVIRONMENT', 'development')
    if env == 'development':
        return Development()
    if env == 'test':
        return Test()
    if env == 'production':
        pass
    