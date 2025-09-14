import time
import httpx

_cache = {"data": None, "ts": 0}
TTL = 600  # 10 minutes

async def fetch_breeds(api_url: str, api_key: str | None):
    global _cache
    now = time.time()
    if _cache["data"] and now - _cache["ts"] < TTL:
        return _cache["data"]
    headers = {"x-api-key": api_key} if api_key else {}
    async with httpx.AsyncClient(timeout=10) as client:
        r = await client.get(api_url, headers=headers)
        r.raise_for_status()
        data = r.json()
    _cache = {"data": data, "ts": now}
    return data

async def validate_breed(name: str, api_url: str, api_key: str | None) -> bool:
    breeds = await fetch_breeds(api_url, api_key)
    names = {b.get("name", "").lower() for b in breeds}
    return name.lower() in names
