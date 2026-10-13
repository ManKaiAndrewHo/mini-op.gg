from puuid import get_PUUID
from match import get_match_history, get_match_details
from db import init_db, save_match, populate_items, populate_summoner_spells, populate_runes
from ddragon import get_latest_version, fetch_items, fetch_summoner_spells, fetch_runes

if __name__ == "__main__":
    conn = init_db()
    
    version = get_latest_version()
    populate_items(conn, fetch_items(version))
    populate_summoner_spells(conn, fetch_summoner_spells(version))
    populate_runes(conn, fetch_runes(version))

    puuid = get_PUUID("Wuju Senshi", "Yi")
    match_ids = get_match_history(puuid, count=20)

    for match_id in match_ids:
        match_data = get_match_details(match_id)
        save_match(conn, match_data)
        print(f"Saved {match_id}")

    conn.close()