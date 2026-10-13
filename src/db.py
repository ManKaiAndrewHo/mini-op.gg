import psycopg2
import os
import json
from dotenv import load_dotenv
load_dotenv()

def init_db():
    
    def get_connection():
        return psycopg2.connect(os.getenv("DATABASE_URL"))

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS summoners (
            puuid TEXT PRIMARY KEY,
            game_name TEXT NOT NULL,
            tag_line TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS matches (
            match_id TEXT PRIMARY KEY,
            game_duration INTEGER NOT NULL,
            game_mode TEXT NOT NULL,
            game_creation BIGINT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS participants (
            participant_pk SERIAL PRIMARY KEY,
            match_id TEXT NOT NULL REFERENCES matches(match_id),
            puuid TEXT NOT NULL REFERENCES summoners(puuid),
            champion_name TEXT,
            team_position TEXT,
            win BOOLEAN,
            kills INTEGER,
            deaths INTEGER,
            assists INTEGER,
            gold_earned INTEGER,
            total_minions_killed INTEGER,
            vision_score INTEGER,
            UNIQUE (match_id, puuid)
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS items (
            item_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS summoner_spells (
            spell_key INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS rune_trees (
            tree_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL
        )
    """)
    
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS runes (
            rune_id INTEGER PRIMARY KEY,
            name TEXT NOT NULL   
        )
    """)

    conn.commit()
    return conn
    
def save_match(conn, match_data: dict):
    cursor = conn.cursor()
    info = match_data["info"]
    match_id = match_data["metadata"]["matchId"]
    primary_style, sub_style, keystone = extract_runes(p["perks"])

    cursor.execute("""
        INSERT INTO matches (match_id, game_duration, game_mode, game_creation)
        VALUES (%s, %s, %s, %s)
        ON CONFLICT (match_id) DO NOTHING
    """, (match_id, info["gameDuration"], info["gameMode"], info["gameCreation"]))

    for p in info["participants"]:
        cursor.execute("""
            INSERT INTO summoners (puuid, game_name, tag_line)
            VALUES (%s, %s, %s)
            ON CONFLICT (puuid) DO NOTHING
        """, (p["puuid"], p["riotIdGameName"], p["riotIdTagline"]))

        cursor.execute("""
            INSERT INTO participants (
                match_id, puuid, champion_name, team_position, win,
                kills, deaths, assists, gold_earned, total_minions_killed, vision_score,
                item0, item1, item2, item3, item4, item5, item6,
                summoner1_id, summoner2_id, perks, team_id,
                primary_style, sub_style, keystone
            )
            VALUES (%s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s, %s, %s, %s,
            %s, %s, %s, %s,
            %s, %s, %s)
            ON CONFLICT (match_id, puuid) DO NOTHING
        """, (
            match_id, p["puuid"], p["championName"], p["teamPosition"], p["win"],
            p["kills"], p["deaths"], p["assists"], p["goldEarned"],
            p["totalMinionsKilled"], p["visionScore"],
            p["item0"], p["item1"], p["item2"], p["item3"], p["item4"], p["item5"], p["item6"],
            p["summoner1Id"], p["summoner2Id"],
            json.dumps(p["perks"]), p["teamId"],
            primary_style, sub_style, keystone
        ))

    conn.commit()
    
def populate_items(conn, items_data: dict):
    cursor = conn.cursor()
    for item_id, item_data in items_data.items():
        cursor.execute("""
            INSERT INTO items (item_id, name)
            VALUES (%s, %s)
            ON CONFLICT (item_id) DO UPDATE SET name = EXCLUDED.name
        """, (int(item_id,), item_data["name"]))
    conn.commit()
    
def populate_summoner_spells(conn, summoner_spells_data: dict):
    cursor = conn.cursor()
    for spell_key, spell_data in summoner_spells_data.items():
        cursor.execute("""
            INSERT INTO summoner_spells (spell_key, name)
            VALUES (%s, %s)
            ON CONFLICT (spell_key) DO UPDATE SET name = EXCLUDED.name
        """, (int(spell_data["key"]), spell_data["name"]))
    conn.commit()
    
def extract_runes(perks: dict):
    styles = perks.get("styles", [])
    primary = styles[0] if len(styles) > 0 else None
    sub = styles[1] if len(styles) > 1 else None
    
    primary_style = primary["style"] if primary else None
    sub_style = sub["style"] if sub else None
    keystone = None
    if primary and primary.get("selections"):
        keystone = primary["selections"][0]["perk"]
        
    return primary_style, sub_style, keystone

def populate_runes(conn, runes_data: list):
    cursor = conn.cursor()
    for tree in runes_data:
        cursor.execute("""
            INSERT INTO rune_trees (tree_id, name)
            VALUES (%s, %s)
            ON CONFLICT (tree_id) DO UPDATE SET name = EXCLUDED.name
        """, (tree["id"], tree["name"]))
        
        for slot in tree["slots"]:
            for rune in slot["runes"]:
                cursor.execute("""
                    INSERT INTO runes (rune_id, name)
                    VALUES (%s, %s)
                    ON CONFLICT (rune_id) DO UPDATE SET name = EXCLUDED.name
                """, (rune["id"], rune["name"]))
    conn.commit()
    
