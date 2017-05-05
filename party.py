"""Flask site for Balloonicorn's Party."""


from flask import Flask, session, render_template, request, flash, redirect
from flask_debugtoolbar import DebugToolbarExtension
from model import Game, connect_to_db
from flask.ext.sqlalchemy import SQLAlchemy

db = SQLAlchemy()
app = Flask(__name__)
app.secret_key = "SECRETSECRETSECRET"


@app.route("/")
def homepage():
    """Show homepage."""

    return render_template("homepage.html")


@app.route("/rsvp", methods=['POST'])
def rsvp():
    """Register for the party."""

    name = request.form.get("name")
    email = request.form.get("email")

    session['RSVP'] = True
    flash("Yay!")
    return redirect("/")


@app.route("/games")
def games():

    if session.get('RSVP'):
        games = Game.query.all()
        return render_template("games.html", games=games)
    else:
        return redirect("/")

@app.route("/games", methods=['POST'])
def add_game():

    game_name = request.form.get("game-name")
    description = request.form.get("description")

    new_game = Game(name=game_name, description=description)

    db.session.add(new_game)
    db.session.commit()

    return redirect("/games")



if __name__ == "__main__":
    app.debug = True
    app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
    DebugToolbarExtension(app)
    connect_to_db(app)
    app.run()
