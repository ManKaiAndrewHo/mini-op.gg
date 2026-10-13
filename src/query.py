from psycopg2.extras import RealDictCursor

def get_puuid_from_db(conn, game_name: str, tag_line:str):
    