from flask import Flask, request, render_template
from resources import *

app = Flask(__name__)


@app.route("/rents")
def rent_page():
    return render_template("rents_page.html")


@app.route("/poster")
def poster_page():
    return render_template("poster_page.html")


@app.route("/space")
def space_page():
    return render_template("space_page.html")


@app.route("/gallery")
def gallery_page():
    return render_template("gallery_page.html")


@app.route("/guests")
def guests_page():
    return render_template("guests_page.html")


@app.route("/contacts")
def contacts_page():
    return render_template("contacts_page.html")


@app.route("/")
def index():
    return render_template("index.html")


"""@app.route("/style/<name>")
def style(name):
    
    return get_style(name)"""


if __name__ == "__main__":
    app.run(host="localhost", port=80, debug=True)
