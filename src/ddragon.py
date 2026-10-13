import requests

def get_latest_version() -> str:
    url = "https://ddragon.leagueoflegends.com/api/versions.json"
    response = requests.get(url)
    response.raise_for_status()  # raises an error for bad responses
    versions = response.json()
    return versions[0]  # returns the latest version

def fetch_items(version: str) -> dict:
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/item.json"
    response = requests.get(url)
    response.raise_for_status()
    items = response.json()['data']
    return items

def fetch_summoner_spells(version: str) -> dict:
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/summoner.json"
    response = requests.get(url)
    response.raise_for_status()
    summoner_spells = response.json()['data']
    return summoner_spells

def fetch_runes(version: str) -> list:
    url = f"https://ddragon.leagueoflegends.com/cdn/{version}/data/en_US/runesReforged.json"
    response = requests.get(url)
    response.raise_for_status()
    runes = response.json()
    return runes

