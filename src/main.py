from puuid import get_PUUID
from match import get_match_history
from match import get_match_details
from db import init_db, save_match, get_puuid, get_match_ids

if __name__ == "__main__":
    conn = init_db()

    puuid = get_puuid("Wuju Senshi", "Yi")
    match_ids = get_match_ids(puuid, count=20)

    for match_id in match_ids:
        match_data = get_match_details(match_id)
        save_match(conn, match_data)
        print(f"Saved {match_id}")

    conn.close()
    
    # print(puuid)  # prints the PUUID for the given game name and tag line

    # match_history = get_match_history(puuid)
    # print(match_history)  # prints the match history for the given PUUID

    # match_details = get_match_details(match_history[0])
    # print(match_details.keys())  # prints the keys of the details of the first match in the match history
