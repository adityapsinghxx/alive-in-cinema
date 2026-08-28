from flask import Flask, render_template, request, redirect, session
from helpers import (
    get_all_movies,
    recommend_movies,
    get_cinema_dna_statement
)


app = Flask(__name__)

app.secret_key = "alive-in-cinema-development-key"


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


SIGNALS = {

    

    "thoughtful": {
        "psychological": 3,
        "mystery": 1,
        "ambiguity": 2,
        "slow_burn": 1
    },

    "emotional": {
        "character_focus": 3,
        "romance": 2,
        "psychological": 1
    },

    "experience": {
        "action": 2,
        "suspense": 2,
        "slow_burn": -2,
        "comedy": 1
    },

    "light": {
        "comedy": 3,
        "darkness": -3,
        "romance": 1,
        "psychological": -1
    },


    # CHARACTER VS STORY

    "people": {
        "character_focus": 4,
        "psychological": 2,
        "romance": 1
    },

    "character": {
        "character_focus": 4,
        "psychological": 1
    },

    "story": {
        "mystery": 2,
        "suspense": 2,
        "character_focus": -3
    },


    # PACING

    "slow": {
        "slow_burn": 4,
        "character_focus": 1,
        "psychological": 1,
        "action": -2
    },

    "fast": {
        "slow_burn": -4,
        "suspense": 2,
        "action": 2
    },


    # AMBIGUITY / CLARITY

    "guess": {
        "ambiguity": 4,
        "mystery": 3,
        "psychological": 1
    },

    "ambiguity": {
        "ambiguity": 4,
        "psychological": 2,
        "mystery": 1
    },

    "answers": {
        "ambiguity": -4,
        "mystery": -1
    },


    # ATMOSPHERE

    "dark": {
        "darkness": 4,
        "psychological": 2,
        "suspense": 2,
        "comedy": -2
    },


    # TENSION VS SPECTACLE

    "suspense": {
        "suspense": 4,
        "mystery": 2,
        "action": 1
    },

    "action": {
        "action": 4,
        "suspense": 2,
        "slow_burn": -2
    },


    # RELATIONSHIPS VS PSYCHOLOGY

    "romance": {
        "romance": 4,
        "character_focus": 2,
        "darkness": -1
    },

    "psychological": {
        "psychological": 4,
        "character_focus": 1,
        "ambiguity": 1,
        "darkness": 1
    }
}


def calculate_dna(answers):

    dna = {}

    # Start at a neutral 5
    for attribute in DNA_ATTRIBUTES:
        dna[attribute] = 5.0

    # Add each answer's influence
    for answer in answers:

        if answer not in SIGNALS:
            continue

        for attribute, signal in SIGNALS[answer].items():

            dna[attribute] += signal * 0.35

    # Keep scores between 0 and 10
    for attribute in DNA_ATTRIBUTES:

        dna[attribute] = max(
            0.0,
            min(10.0, dna[attribute])
        )

        dna[attribute] = round(
            dna[attribute],
            2
        )

    return dna

QUESTIONS = [

    {
        "question": "What do you want a movie to do to you?",
        "options": [
            (
                "thoughtful",
                "Make me think",
                "Give me ideas, questions, or something to discuss after it ends."
            ),
            (
                "emotional",
                "Make me feel",
                "Give me an emotional experience that stays with me."
            ),
            (
                "experience",
                "Give me a great experience",
                "Immerse me and make the two or three hours fly by."
            ),
            (
                "light",
                "Just let me have fun",
                "Make me laugh, smile, or simply have a great time."
            )
        ]
    },


    {
        "question": "Which kind of story sounds more appealing?",
        "options": [
            (
                "people",
                "A fascinating character",
                "I want to understand a person and become invested in their journey."
            ),
            (
                "story",
                "An incredible story",
                "Give me a plot that keeps unfolding and surprises me."
            )
        ]
    },


    {
        "question": "How much patience do you have for a movie?",
        "options": [
            (
                "slow",
                "Take your time",
                "I enjoy atmosphere, buildup, and stories that unfold gradually."
            ),
            (
                "fast",
                "Keep me hooked",
                "I want the story moving and something happening."
            )
        ]
    },


    {
        "question": "What kind of mystery sounds better?",
        "options": [
            (
                "guess",
                "Make me figure it out",
                "I love hidden meanings, clues, unanswered questions, and ambiguity."
            ),
            (
                "answers",
                "Tell me the story",
                "I prefer a clear narrative with satisfying answers."
            )
        ]
    },


    {
        "question": "What kind of atmosphere would you choose tonight?",
        "options": [
            (
                "dark",
                "Dark & unsettling",
                "Something disturbing, intense, eerie, or emotionally heavy."
            ),
            (
                "light",
                "Warm & uplifting",
                "Something charming, comforting, funny, or positive."
            )
        ]
    },


    {
        "question": "What sounds more exciting?",
        "options": [
            (
                "suspense",
                "Sitting on the edge of my seat",
                "Tension, anticipation, danger, and wondering what happens next."
            ),
            (
                "action",
                "Pure cinematic spectacle",
                "Big moments, physical intensity, set pieces, and adrenaline."
            )
        ]
    },


    {
        "question": "Which emotional experience appeals to you more?",
        "options": [
            (
                "romance",
                "A powerful relationship",
                "Love, connection, chemistry, and complicated relationships."
            ),
            (
                "psychological",
                "Getting inside someone's head",
                "Exploring identity, obsession, trauma, ambition, or human behavior."
            )
        ]
    },


    {
        "question": "How do you feel about complicated movies?",
        "options": [
            (
                "ambiguity",
                "Give me something to decode",
                "I enjoy interpreting a movie and forming my own conclusions."
            ),
            (
                "answers",
                "Give me a satisfying story",
                "I don't want to work too hard to understand what happened."
            )
        ]
    },


    {
        "question": "What matters more to you in a great movie?",
        "options": [
            (
                "character",
                "Characters I care about",
                "Great performances and characters can carry a movie for me."
            ),
            (
                "story",
                "A story I can't stop thinking about",
                "A brilliant premise, plot, or narrative can carry the movie for me."
            )
        ]
    },


    {
        "question": "What would make you recommend a movie to a friend?",
        "options": [
            (
                "emotional",
                "It made me feel something",
                "I want a movie that creates a powerful emotional reaction."
            ),
            (
                "experience",
                "I've never seen anything like it",
                "Originality, creativity, spectacle, or a unique experience."
            )
        ]
    }

]



@app.route("/")
def index():

    return render_template("index.html")


@app.route("/quiz", methods=["GET", "POST"])
def quiz():

    if request.method == "POST":

        answer = request.form.get("answer")

        if answer:

            answers = session.get(
                "answers",
                []
            )

            answers.append(answer)

            session["answers"] = answers

        question_number = int(
            request.form.get(
                "question_number",
                0
            )
        )

        # Quiz is finished
        if question_number + 1 >= len(QUESTIONS):

            answers = session.get(
                "answers",
                []
            )

            dna = calculate_dna(answers)

            session["cinema_dna"] = dna

            return redirect("/profile")

        # Go to next question
        return redirect(
            f"/quiz?question={question_number + 1}"
        )


    question_number = int(
        request.args.get(
            "question",
            0
        )
    )


    # Start a fresh quiz
    if question_number == 0:

        session["answers"] = []


    if question_number >= len(QUESTIONS):

        return redirect("/profile")


    question = QUESTIONS[question_number]


    return render_template(
        "quiz.html",
        question=question,
        question_number=question_number,
        total_questions=len(QUESTIONS)
    )


@app.route("/profile")
def profile():

    answers = session.get(
        "answers",
        []
    )

    dna = session.get(
        "cinema_dna",
        calculate_dna(answers)
    )

    session["cinema_dna"] = dna

    recommendations = recommend_movies(
        dna
    )

    cinema_statement = get_cinema_dna_statement(
        dna
    )

    return render_template(
        "profile.html",
        answers=answers,
        dna=dna,
        recommendations=recommendations,
        cinema_statement=cinema_statement
    )

@app.route("/reset")
def reset():

    session.clear()

    return redirect("/")


if __name__ == "__main__":

    app.run(
        debug=True
    )
