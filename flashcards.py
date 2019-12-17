from flask import Flask, render_template
from model import db

app = Flask(__name__)


@app.route("/")
def welcome():
    return render_template('welcome.html')


@app.route("/card/<int:index>")
def card_view(index):
    card = db[index]
    return render_template("card.html", card=card)
