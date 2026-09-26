import psycopg2
import os

def init_db():
    conn = psycopg2.connect(os.getenv("DATABASE_URL"))
    cursor = conn.cursor()
    
    cursor.execute("""
        CREATE TABLE IF NOT EXITS summoners (
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
            game_creation BIGINT NOT NULL,
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
            vision_score INTEGER
        )           
    """)
    
    conn.commit()
    return conn

def save_match(conn, match_data: dict):
    cursor = conn.cursor()
    info = match_data["info"]
    match_id = match_data["metadata"]["matchId"]
    
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
        """, (p["puuid"], p["summonerName"], p["summonerId"]))
        
        cursor.execute("""
            INSERT INTO participants (match_id, puuid, champion_name, team_position, win, kills, deaths, assists, gold_earned, total_minions_killed, vision_score)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (match_id, puuid) DO NOTHING
        """, (
            match_id, p["puuid"], p["championName"], p["teamPosition"],
            p["win"], p["kills"], p["deaths"], p["assists"],
            p["goldEarned"], p["totalMinionsKilled"], p["visionScore"]))
        
    conn.commit()
    
    