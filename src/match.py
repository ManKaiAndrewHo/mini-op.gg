from puuid import get_PUUID
from dotenv import load_dotenv
import os
import requests
from urllib.parse import quote

load_dotenv()  # reads .env and loads it into environment variables

api_key = os.getenv("RIOT_API_KEY")
# print(api_key)  # sanity check — remove this line once it works

def get_match_history(puuid: str, region: str = "americas", count: int = 20) -> list[str]:
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuid}/ids?start=0&count={count}&api_key={api_key}"
    respond = requests.get(url)
    respond.raise_for_status()  # raises an error for bad responses
    return respond.json()  # returns a list of match IDs

def get_match_details(match_id: str, region: str = "americas") -> dict:
    url = f"https://{region}.api.riotgames.com/lol/match/v5/matches/{match_id}?api_key={api_key}"
    respond = requests.get(url)
    respond.raise_for_status()  # raises an error for bad responses
    return respond.json()  # returns the match details