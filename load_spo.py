import extract_spo as ex
import transform_spo as tr
import sqlalchemy
import pandas as pd
from sqlalchemy.orm import sessionmaker
import requests
import json
from datetime import datetime
import datetime
import sqlite3

DATABASE_LOC = "sqlite:///recently_played_tracks.sqlite"


# there's currently an issue with the data quality function, maybe might need to create a new primary key as it says the current IDs are not unique (there might be a duplicate)
if __name__ == "__main__":
    load_df=ex.create_recently_played_df()
    if (tr.Data_Quality(load_df) == False):
        raise ("Failed Data Validation - check data in source")
    
    engine = sqlalchemy.create_engine(DATABASE_LOC)
    conn = sqlite3.connect('recently_played_tracks.sqlite')
    cur = conn.cursor()

    create_song_table = """
    CREATE TABLE IF NOT EXISTS recently_played_tracks(
        name VARCHAR(200),
        artist VARCHAR(200),
        ID INTEGER(100) PRIMARY KEY,
    )
    """

    
    cur.execute(create_song_table)

    print("Database initialized with new table")

    try:
        load_df.to_sql("recently_played_tracks", engine, index=False, if_exists='append')
    except:
        print("Previous data exists in the database already.")
    
    conn.close()
    print("Connection to database successfully closed")