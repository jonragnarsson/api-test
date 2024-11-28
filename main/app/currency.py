from typing import List
from time import time
from urllib import request
from urllib.error import HTTPError, URLError
import json
from pprint import pp
from .config import Config


class Currency:
    _url = ''
    _currency: dict = {}
    _age_minutes: float = 0
    _keep: List = ['GBP', 'DKK', 'SWE', 'ISK', 'NOK', 'USD', 'EUR']
    
    def __init__(self, settings: Config):
        self._url = settings.URL_WITH_KEY
        self._keep = settings.AVAILABLE_SYMBOLS
    
    async def valid(self, base: str) -> bool:
        return base in self._keep
    
    async def all(self):
        return self._keep
    
    async def get(self, base: str = 'NOK') -> dict:
        # Not neccesary with fastapi-cache
        #if (self._age_minutes + (60 * 60) > time()) and base in self._currency:
        #    return self._currency[base]
        #self._age_minutes = time()
        tlist = []
        basevalue = 1
        try:
            with request.urlopen(self._url, timeout=20) as url:
                data = json.loads(url.read().decode())
                for k in data['rates'].items():
                    if k[0] == base:
                        basevalue = k[1]
                    if k[0] in self._keep:
                        tlist.append(k)
        except HTTPError as error:
            return {'error': error.reason, 'status': error.status}
        except URLError as error:
            return {'error': error.reason, 'status': error.errno}

        self._currency[base] = {}
        for l in tlist:
            if l[0] != base:
                f = basevalue / l[1]
                self._currency[base][l[0]] = f
        return self._currency[base]

    async def convert(self, cfrom, cto):
        if cfrom == cto:
            return 1
        base = await self.get(cfrom)
        return base[cto]
    
    async def clear(self, base: str | None = None) -> None:
        if base:
            self._currency[base] = None
        else:
            self._currency = {}
