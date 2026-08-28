import csv
import sqlite3


DATABASE = "cinema.db"
CSV_FILE = "alive_in_cinema_50_movies.csv"


connection = sqlite3.connect(DATABASE)

db = connection.cursor()


# Create movies table

db.execute("""
    CREATE TABLE IF NOT EXISTS movies (
        id INTEGER PRIMARY KEY,
        title TEXT NOT NULL,
        year INTEGER,
        country TEXT,
        language TEXT,
        genres TEXT
    )
""")


# Create movie attributes table

db.execute("""
    CREATE TABLE IF NOT EXISTS movie_attributes (
        movie_id INTEGER PRIMARY KEY,

        psychological INTEGER,
        darkness INTEGER,
        mystery INTEGER,
        suspense INTEGER,
        action INTEGER,
        comedy INTEGER,
        romance INTEGER,
        slow_burn INTEGER,
        ambiguity INTEGER,
        character_focus INTEGER,

        FOREIGN KEY (movie_id)
            REFERENCES movies(id)
    )
""")


# Read the CSV file

with open(CSV_FILE, newline="", encoding="utf-8") as file:

    reader = csv.DictReader(file)

    for row in reader:

        db.execute("""
            INSERT OR REPLACE INTO movies
            (id, title, year, country, language, genres)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            row["id"],
            row["title"],
            row["year"],
            row["country"],
            row["language"],
            row["genres"]
        ))


        db.execute("""
            INSERT OR REPLACE INTO movie_attributes
            (
                movie_id,
                psychological,
                darkness,
                mystery,
                suspense,
                action,
                comedy,
                romance,
                slow_burn,
                ambiguity,
                character_focus
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            row["id"],
            row["psychological"],
            row["darkness"],
            row["mystery"],
            row["suspense"],
            row["action"],
            row["comedy"],
            row["romance"],
            row["slow_burn"],
            row["ambiguity"],
            row["character_focus"]
        ))


connection.commit()


# Check how many movies were imported

db.execute("SELECT COUNT(*) FROM movies")

count = db.fetchone()[0]

print(f"Imported {count} movies.")


connection.close()
