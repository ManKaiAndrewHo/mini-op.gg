from dotenv import load_dotenv
import os
import requests
from urllib.parse import quote

load_dotenv()  # reads .env and loads it into environment variables

api_key = os.getenv("RIOT_API_KEY")
# print(api_key)  # sanity check — remove this line once it works

def get_PUUID(game_name: str, tag_line: str, region: str = "americas") -> str:
    game_name = quote(game_name)
    tag_line = quote(tag_line)
    url = f"https://{region}.api.riotgames.com/riot/account/v1/accounts/by-riot-id/{game_name}/{tag_line}?api_key={api_key}"

    response = requests.get(url)
    response.raise_for_status()  # raises an error for bad responses
    print(response.status_code)  # prints the HTTP status code for debugging
    
    data = response.json()
    # print(data)  # prints the entire JSON response for debugging
    return data.get("puuid")

