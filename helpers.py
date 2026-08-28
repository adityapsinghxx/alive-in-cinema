import sqlite3


DATABASE = "cinema.db"


def get_db_connection():
    connection = sqlite3.connect(DATABASE)
    connection.row_factory = sqlite3.Row
    return connection


def get_all_movies():

    connection = get_db_connection()

    movies = connection.execute("""
        SELECT
            movies.id,
            movies.title,
            movies.year,
            movies.country,
            movies.language,
            movies.genres,

            movie_attributes.psychological,
            movie_attributes.darkness,
            movie_attributes.mystery,
            movie_attributes.suspense,
            movie_attributes.action,
            movie_attributes.comedy,
            movie_attributes.romance,
            movie_attributes.slow_burn,
            movie_attributes.ambiguity,
            movie_attributes.character_focus

        FROM movies

        JOIN movie_attributes
        ON movies.id = movie_attributes.movie_id
    """).fetchall()

    connection.close()

    return movies


DNA_ATTRIBUTES = [
    "psychological",
    "darkness",
    "mystery",
    "suspense",
    "action",
    "comedy",
    "romance",
    "slow_burn",
    "ambiguity",
    "character_focus"
]


def calculate_movie_match(user_dna, movie):

    total_difference = 0

    for attribute in DNA_ATTRIBUTES:

        user_score = user_dna[attribute]
        movie_score = movie[attribute]

        difference = abs(user_score - movie_score)

        total_difference += difference

    maximum_difference = 10 * len(DNA_ATTRIBUTES)

    similarity = 1 - (
        total_difference / maximum_difference
    )

    return round(similarity * 100, 1)


def get_match_dimensions(user_dna, movie):

    differences = []

    for attribute in DNA_ATTRIBUTES:

        difference = abs(
            user_dna[attribute] - movie[attribute]
        )

        differences.append(
            (attribute, difference)
        )

    differences.sort(
        key=lambda item: item[1]
    )

    return [
        attribute
        for attribute, difference in differences[:3]
    ]


def get_match_explanation(match_dimensions):

    descriptions = {

        "psychological":
            "psychological depth",

        "darkness":
            "darker themes",

        "mystery":
            "mystery and unanswered questions",

        "suspense":
            "suspense and tension",

        "action":
            "action and intensity",

        "comedy":
            "humour and lighter moments",

        "romance":
            "romance and emotional connection",

        "slow_burn":
            "slow-burning storytelling",

        "ambiguity":
            "ambiguity and room for interpretation",

        "character_focus":
            "character-driven storytelling"
    }

    qualities = [
        descriptions[attribute]
        for attribute in match_dimensions
    ]

    if len(qualities) == 3:

        return (
            "Your Cinema DNA connects strongly with this film "
            "through its {}, {}, and {}."
        ).format(
            qualities[0],
            qualities[1],
            qualities[2]
        )

    return (
        "Your Cinema DNA connects strongly with this film."
    )


def get_cinema_dna_statement(user_dna):

    # Find the user's three strongest DNA dimensions.
    strongest = sorted(
        DNA_ATTRIBUTES,
        key=lambda attribute: user_dna[attribute],
        reverse=True
    )[:3]


    statements = {

        ("psychological", "mystery", "ambiguity"):
            "You are drawn to stories that get inside the mind, keep you questioning what is real, and leave room for your own interpretation.",

        ("psychological", "character_focus", "slow_burn"):
            "You are drawn to patient, character-driven stories that explore what is happening beneath the surface.",

        ("psychological", "darkness", "ambiguity"):
            "You gravitate toward darker stories that explore the mind, challenge your perspective, and leave you with questions.",

        ("mystery", "suspense", "ambiguity"):
            "You like stories that keep you guessing, build tension, and leave just enough unanswered for you to figure out.",

        ("mystery", "suspense", "action"):
            "You want stories that keep unfolding, keep you guessing, and give you enough intensity to stay completely engaged.",

        ("action", "suspense", "fast"):
            "You want cinema that moves — tension, intensity, and moments that keep you locked in.",

        ("action", "suspense", "darkness"):
            "You gravitate toward intense cinema where danger, tension, and darker themes keep the experience alive.",

        ("romance", "character_focus", "emotional"):
            "You connect most with films built around people, relationships, and emotions that stay with you.",

        ("romance", "comedy", "character_focus"):
            "You enjoy films that balance heart and lighter moments with characters you genuinely care about.",

        ("comedy", "romance", "light"):
            "You like cinema that makes you feel good — warm relationships, humour, and an experience that leaves you smiling.",

        ("slow_burn", "psychological", "character_focus"):
            "You have patience for stories that take their time, build atmosphere, and dig deeply into their characters.",

        ("slow_burn", "mystery", "psychological"):
            "You enjoy stories that unfold patiently, build intrigue, and reward you for paying attention.",

        ("darkness", "psychological", "suspense"):
            "You are drawn to darker, intense stories that explore human behaviour and keep tension simmering beneath the surface."
    }


    key = tuple(strongest)

    if key in statements:

        return statements[key]


    descriptions = {

        "psychological":
            "psychological depth",

        "darkness":
            "darker themes",

        "mystery":
            "mystery",

        "suspense":
            "tension",

        "action":
            "action and intensity",

        "comedy":
            "humour",

        "romance":
            "romance and emotional connection",

        "slow_burn":
            "slow-burning storytelling",

        "ambiguity":
            "ambiguity and interpretation",

        "character_focus":
            "character-driven storytelling"
    }


    qualities = [
        descriptions[attribute]
        for attribute in strongest
    ]


    return (
        "You are drawn to cinema shaped by {}, {}, and {}."
    ).format(
        qualities[0],
        qualities[1],
        qualities[2]
    )


def recommend_movies(user_dna):

    movies = get_all_movies()

    recommendations = []

    for movie in movies:

        match = calculate_movie_match(
            user_dna,
            movie
        )

        match_dimensions = get_match_dimensions(
            user_dna,
            movie
        )

        explanation = get_match_explanation(
            match_dimensions
        )

        recommendations.append({
            "movie": movie,
            "match": match,
            "match_dimensions": match_dimensions,
            "explanation": explanation,
            "poster" : get_poster_filename(movie["title"])
        })

    recommendations.sort(
        key=lambda item: item["match"],
        reverse=True
    )

    return recommendations[:5]


def refine_dna_with_choice(user_dna, chosen_movie, rejected_movie):

    refined_dna = user_dna.copy()

    for attribute in DNA_ATTRIBUTES:

        chosen_score = chosen_movie[attribute]
        rejected_score = rejected_movie[attribute]

        difference = chosen_score - rejected_score

        # Small adjustment so movie choices refine,
        # rather than completely replace, the quiz profile.
        adjustment = difference * 0.08

        refined_dna[attribute] += adjustment

        refined_dna[attribute] = max(
            0,
            min(10, refined_dna[attribute])
        )

    return refined_dna

def get_poster_filename(movie_title):

    posters = {
        "Interstellar": "interstellar.jpg",
        "The Martian": "the-martian.jpg",
        "Mad Max: Fury Road": "mad-max-fury-road.jpg",
        "The Revenant": "the-revenant.jpg",
        "Deadpool": "deadpool.jpg",
        "La La Land": "lalaland.jpg",
        "Arrival": "arrival.jpg",
        "Get Out": "getout.jpg",
        "Dunkirk": "dunkirk.jpg",
        "Blade Runner 2049": "blade-runner-2049.jpg",
        "Avengers: Infinity War": "avengers-infinity-war.jpg",
        "Spider-Man: Into the Spider-Verse": "spiderman-into-the-spider-verse.jpg",
        "A Quiet Place": "a-quiet-place.jpg",
        "Joker": "joker.jpg",
        "Parasite": "parasite.jpg",
        "Avengers: Endgame": "avengers-end-game.jpg",
        "Knives Out": "knives-out.jpg",
        "Everything Everywhere All at Once": "everything-everywhere-all-at-once.jpg",
        "Top Gun: Maverick": "top-gun-maverick.jpg",
        "The Batman": "the-batman.jpg",
        "Oppenheimer": "oppenheimer.jpg",
        "Barbie": "barbie.jpg",
        "Guardians of the Galaxy Vol. 3": "guardians-of-the-galaxy-vol-3.jpg",
        "Dune: Part Two": "dune-part-two.jpg",
        "Inside Out 2": "inside-out.jpg",
        "Deadpool & Wolverine": "deadpool-and-wolverine.jpg",
        "F1": "f1.jpg",
        "Superman": "superman.jpg",
        "The Godfather": "the-godfather.jpg",
        "Rocky": "rocky.jpg",
        "The Shining": "the-shining.jpg",
        "Back to the Future": "back-to-the-future.jpg",
        "The Silence of the Lambs": "the-silence-of-the-lambs.jpg",
        "Goodfellas": "goodfellas.jpg",
        "Forrest Gump": "forrest-gump.jpg",
        "Fight Club": "fight-club.jpg",
        "The Matrix": "the-matrix.jpg",
        "The Dark Knight": "the-dark-knight.jpg",
        "The Lord of the Rings: The Fellowship of the Ring":
            "the-lord-of-the-rings-the-fellowship-of-the-ring.jpg",
        "Titanic": "titanic.jpg",
        "3 Idiots": "3-idiots.jpg",
        "Dangal": "dangal.jpg",
        "Andhadhun": "andhadhun.jpg",
        "Gully Boy": "gully-boy.jpg",
        "Animal": "animal.jpg",
        "Chhaava": "chhaava.jpg",
        "Baahubali: The Beginning": "bahubali-the-beginning.jpg",
        "RRR": "rrr.jpg",
        "Kantara": "kantara.jpg",
        "Manjummel Boys": "manjummel-boys.jpg"
    }

    return posters.get(movie_title)



# AI assistance was used during development for debugging,troubleshooting, implementation guidance.
