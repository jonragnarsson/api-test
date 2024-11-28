from fastapi import FastAPI, HTTPException
from fastapi_cache import FastAPICache
from fastapi_cache.backends.inmemory import InMemoryBackend
from fastapi_cache.decorator import cache

from .config import env
from .currency import Currency
memcache = InMemoryBackend()
FastAPICache.init(memcache, prefix='wat')
app = FastAPI()
currencyserv = Currency(env())


@app.get("/")
@cache(expire=100)
async def root():
    return {'available': await currencyserv.all()}


#@app.get('/invalidate/{currency}')
@app.get('/invalidate')
async def invalidate(currency: str | None = None):
    await memcache.clear(currency)
    await currencyserv.clear(currency)
    return 'Cache cleared'


@app.get('/{base}')
@cache(expire=100)
async def base(base: str):
    if await currencyserv.valid(base):
        data = await currencyserv.get(base)
        if 'error' in data:
            return HTTPException(status_code=500, detail=data.get('status', ''))  # terrible
        return data
    raise HTTPException(status_code=404, detail="fCurrency '{base}' not found")


@app.get('/{cfrom}/{cto}')
@cache(expire=100)
async def convert(cfrom: str, cto: str):
    if not await currencyserv.valid(cfrom):
        raise HTTPException(status_code=404, detail=f"Currency '{cfrom}' not found")
    if not await currencyserv.valid(cto):
        raise HTTPException(status_code=404, detail=f"Currency '{cto}' not found")
    data = await currencyserv.convert(cfrom, cto)
    return data


