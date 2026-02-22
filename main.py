from flask import Flask, render_template, request, jsonify, make_response
from werkzeug.utils import redirect

from concerts_database import DataBase

app = Flask(__name__)
database = DataBase()


def get_all_userdata():
    user_id = request.cookies.get("user_id")
    if user_id is None:
        return None
    return_data = database.get_all_user_info(user_id)
    if return_data["success"]:
        return return_data["data"]
    return None


def get_base_userdata():
    user_id = request.cookies.get("user_id")
    if user_id is None:
        return {"is_placeholder": True, "name": "Anonymous", "photo": "static/images/user_avatar_placeholder.png"}
    return_data = database.get_base_user_info(user_id)
    if return_data["success"]:
        data = return_data["data"]
        data["is_placeholder"] = False
        return data
    return {"is_placeholder": True, "name": "Anonymous", "photo": "static/images/user_avatar_placeholder.png"}


@app.route("/profile")
def profile_page():
    userdata = get_all_userdata()
    return render_template("profile_page.html", userdata=userdata)


@app.route("/register", methods=["POST"])
def register_user():
    username = request.form.get('username')
    password = request.form.get('password')
    nickname = request.form.get('nickname')
    email = request.form.get('email')

    repeat_password = request.form.get('repeat_password')
    if password != repeat_password:
        return "Пароли не совпадают", 400

    userdata = {
        'username': username,
        'password': password,
        'name': nickname,
        'email': email
    }

    if not username:
        return "Missing username", 400
    if not password:
        return "Missing password", 400

    result = database.add_user(userdata, None)

    if result["success"]:
        response = make_response(redirect('profile'))
        response.set_cookie('user_id', str(result.get("user_id")), max_age=30 * 24 * 60 * 60)
        response.set_cookie('username', username, max_age=30 * 24 * 60 * 60)
        return response
    else:
        return f"Ошибка: {result['error']}", 400


@app.route("/rents")
def rent_page():
    return render_template("rents_page.html")


@app.route("/poster")
def poster_page():
    return render_template("poster_page.html")


@app.route("/space")
def space_page():
    userdata = get_base_userdata()
    return render_template("space_page.html", userdata=userdata)


@app.route("/gallery")
def gallery_page():
    userdata = get_base_userdata()
    return render_template("gallery_page.html", userdata=userdata)


@app.route("/guests")
def guests_page():
    return render_template("guests_page.html")


@app.route("/contacts")
def contacts_page():
    userdata = get_base_userdata()
    return render_template("contacts_page.html", userdata=userdata)


@app.route("/add_event")
def add_event_page():
    userdata = get_base_userdata()
    if userdata["is_placeholder"]:
        return redirect("register")


@app.route("/login")
def login_page():
    userdata = get_base_userdata()
    return render_template("login_page.html", userdata=userdata)


@app.route("/register")
def register_page():
    userdata = get_base_userdata()
    return render_template("register_page.html", userdata=userdata)


@app.route("/")
def index():
    concerts = database.get_closest_concerts()
    userdata = get_base_userdata()
    return render_template("index.html", concerts=concerts, userdata=userdata)


"""@app.route("/style/<name>")
def style(name):
    
    return get_style(name)"""

if __name__ == "__main__":
    app.run(host="localhost", port=80, debug=True)
