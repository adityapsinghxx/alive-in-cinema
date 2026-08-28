# Alive in Cinema

#### Video Demo:

https://youtube.com/shorts/DjHVjuhOtEM?si=IvMJbD7DSkw-7Oex

#### Description:

Alive in Cinema is a movie recommendation web application that helps users discover what kind of movies they actually enjoy.

Instead of simply asking users to select their favorite genres, the application uses a short quiz to understand different aspects of their cinematic preferences. The answers are converted into a personalized "Cinema DNA" profile consisting of ten dimensions: psychological depth, darkness, mystery, suspense, action, comedy, romance, slow-burn storytelling, ambiguity, and character focus.

The goal of the project is to make movie recommendations feel more personal and meaningful. Rather than simply saying that a user likes a particular genre, Alive in Cinema attempts to understand the qualities of storytelling that attract them.

### How It Works

The application begins with a simple homepage that introduces Alive in Cinema and allows the user to start the quiz.

The quiz consists of multiple questions. Each answer contributes to one or more dimensions of the user's Cinema DNA. After completing the quiz, the application calculates the user's scores across the ten dimensions.

The resulting Cinema DNA is displayed visually using horizontal score bars. The application also generates a short description of the user's cinematic personality based on their strongest dimensions.

The user's Cinema DNA is then compared against the Movie DNA stored for the movies in the application's database. Each movie has its own scores across the same ten dimensions.

### Movie Recommendation System

The recommendation system compares the user's Cinema DNA with the Movie DNA of every movie in the database.

For each dimension, the application calculates the absolute difference between the user's score and the movie's score. These differences are combined into an overall similarity score.

The maximum possible difference is calculated from all ten dimensions. The resulting similarity value is converted into a percentage match.

The movies are then sorted from highest match to lowest match, and the five strongest matches are displayed to the user.

The application also identifies the dimensions where the user's Cinema DNA and a movie's profile are most closely aligned. These dimensions are used to generate an explanation for why a particular movie is a strong match.

### Database

Alive in Cinema uses SQLite as its database.

The database contains two main pieces of information:

- `movies` stores information such as movie title, year, country, language, and genres.
- `movie_attributes` stores the ten Movie DNA attributes associated with each movie.

Keeping the movie information and its attributes in the database allows the recommendation system to compare the user's profile against the complete movie collection.

### Project Structure

The main files and directories are:

- `app.py` — the Flask application and the main routes that control the web application.
- `helpers.py` — contains the movie retrieval, Cinema DNA matching, recommendation, explanation, and poster-mapping logic.
- `setup_db.py` — creates and populates the SQLite database.
- `cinema.db` — the SQLite database containing the movies and their Movie DNA attributes.
- `requirements.txt` — lists the external Python dependency required by the project.
- `templates/` — contains the HTML/Jinja templates used by the application.
- `static/style.css` — contains the styling and visual design of the application.
- `static/posters/` — contains the local movie poster images used on the recommendation page.
- `alive_in_cinema_50_movies.csv` — contains the movie dataset used to populate the database.

### Design

I wanted Alive in Cinema to feel more like a cinematic editorial experience than a traditional quiz website.

The visual design uses a restrained color palette, serif typography for major headings, minimal borders, large whitespace, and subtle hover interactions. The Cinema DNA results are presented as a visual profile rather than only as numbers.

The recommendation section gives the strongest match additional visual emphasis while displaying the remaining recommendations as individual movie cards with their corresponding posters.

The application is also designed to work across different screen sizes.

### Why I Built It

I built Alive in Cinema because movie recommendations often focus primarily on genres, ratings, or popular titles. I wanted to experiment with a different approach: understanding the characteristics of stories that a person responds to and using those characteristics to create recommendations.

This project allowed me to combine several concepts I learned through CS50, including Flask, Jinja templates, SQLite databases, Python functions, HTML, CSS, and application logic.

More importantly, it gave me the opportunity to build something from an idea into a complete working web application.

### Technologies Used

- Python
- Flask
- SQLite
- Jinja
- HTML
- CSS
- JavaScript

### Running the Application

To run Alive in Cinema locally, install the dependencies:

```bash
pip install -r requirements.txt
