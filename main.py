"""_
Top 10 Movies Website
"""
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from sqlalchemy import desc
from wtforms import StringField, SubmitField, HiddenField
from wtforms.validators import DataRequired
from TMDB import Tmdb

app = Flask(__name__)
app.config["SECRET_KEY"] = "SECRET KEY"
Bootstrap(app)

db = SQLAlchemy()
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///movies.db"
db.init_app(app)

tmdb_instance = Tmdb()


## Create Movies DB
class Movies(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(250), unique=True, nullable=False)
    year = db.Column(db.Integer, nullable=False)
    description = db.Column(db.String(250), nullable=False)
    rating = db.Column(db.Float, nullable=True)
    ranking = db.Column(db.Integer, nullable=True)
    review = db.Column(db.String(250), nullable=True)
    img_url = db.Column(db.String(250), nullable=False)


with app.app_context():
    db.create_all()


class EditForm(FlaskForm):
    """Create a form on the edit page"""

    movie_id = HiddenField()
    rating = StringField("Your rating out of 10", validators=[DataRequired()])
    review = StringField("Your review", validators=[DataRequired()])
    submit = SubmitField("Update")


class AddForm(FlaskForm):
    """Create a form on the add page"""

    movie_id = HiddenField()
    movie_to_add = StringField("Movie Title", validators=[DataRequired()])
    submit = SubmitField("Add Movie")


@app.route("/")
def home():
    movies = Movies.query.order_by(desc(Movies.rating)).all()
    return render_template("index.html", movies=movies)


@app.route("/edit", methods=["GET", "POST"])
def edit():
    form = EditForm()
    if form.validate_on_submit():
        movie = Movies.query.get(form.movie_id.data)
        if movie is None:
            return "Movie not found"
        movie.rating = float(form.rating.data)
        movie.review = form.review.data
        db.session.commit()
        return redirect(url_for("home"))
    movie_id = request.args.get("id")
    movie = Movies.query.get(movie_id)
    form.movie_id.data = movie_id
    return render_template("edit.html", movie=movie, form=form)


@app.route("/delete", methods=["GET", "POST"])
def delete():
    movie_id = request.args.get("id")
    movie_to_delete = Movies.query.get(movie_id)
    db.session.delete(movie_to_delete)
    db.session.commit()
    return redirect(url_for("home"))


@app.route("/add", methods=["GET", "POST"])
def add():
    form = AddForm()
    if form.validate_on_submit():
        movie_to_add = form.movie_to_add.data
        results = tmdb_instance.movie_input(movie_to_add)
        clean_results = tmdb_instance.clean_results(results)
        return render_template("select.html", results=clean_results)
    return render_template("add.html", form=form)


@app.route("/select", methods=["GET", "POST"])
def select():
    form = EditForm()
    movie_id = request.args.get("id")
    movie_details = tmdb_instance.movie_id(movie_id)
    new_movie = Movies(
        id=movie_details["id"],
        title=movie_details["original_title"],
        year=movie_details["release_date"][:4],
        description=movie_details["overview"],
        img_url=f"https://image.tmdb.org/t/p/original{movie_details['poster_path']}",
    )
    db.session.add(new_movie)
    db.session.commit()
    movie_id = request.args.get("id")
    movie = Movies.query.get(movie_id)
    form.movie_id.data = movie_id
    return render_template("edit.html", movie=movie, form=form)


if __name__ == "__main__":
    app.run(debug=True)
