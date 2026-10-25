from psycopg2.extras import RealDictCursor

def get_puuid_from_db(conn, game_name: str, tag_line:str):
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("""
            SELECT puuid
            FROM summoners
            WHERE game_name = %s AND tag_line = %s
        """, (game_name, tag_line))
        row = cursor.fetchone()
        return row["puuid"] if row else None
    
def get_recent_matches(conn, puuid: str, limit: int = 10) -> list[dict]:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("""
            SELECT m.match_id, to_timestamp(m.game_creation / 1000) AS played_at, m.game_mode, 
            p.champion_name, p.win, p.kills, p.deaths, p.assists
            FROM participants p
            JOIN matches m ON p.match_id = m.match_id
            WHERE p.puuid = %s
            ORDER BY m.game_creation DESC
            LMIT %s
        """, (puuid, limit))
        return cursor.fetchall()
    
def get_match_scoreboard(conn, match_id: str) -> list[dict]:
    with conn.cursor(cursor_factory=RealDictCursor) as cursor:
        cursor.execute("""
            SELECT s.game_name, s.tag_line, p.champion_name, p.team_id,
            p.team_position, p.win, p.kills, p.deaths, p.assists, 
            i0.name as item0, i1.name as item1, i2.name as item2, i3.name as item3,
            i4.name as item4, i5.name as item5, i6.name as item6,
            ss1.name as summoner1, ss2.name as summoner2
            FROM participants p
            JOIN summoners s ON p.puuid = s.puuid
            LEFT JOIN items i0 ON p.item0 = i0.item_id
            LEFT JOIN items i1 ON p.item1 = i1.item_id
            LEFT JOIN items i2 ON p.item2 = i2.item_id
            LEFT JOIN items i3 ON p.item3 = i3.item_id
            LEFT JOIN items i4 ON p.item4 = i4.item_id
            LEFT JOIN items i5 ON p.item5 = i5.item_id
            LEFT JOIN items i6 ON p.item6 = i6.item_id
            LEFT JOIN summoner_spell ss1 ON p.summoner1_id = ss1.spell_key
            LEFT JOIN summoner_spell ss2 ON p.summoner2_id = ss2.spell_key
            WHERE p.match_id = %s
            ORDER BY p.team_id, p.participant_pk
        """, (match_id,))
        return cursor.fetchall()