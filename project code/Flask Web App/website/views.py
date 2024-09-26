from flask import Blueprint,render_template

views = Blueprint('views',__name__)

@views.route("/")
@views.route("/home")
def home():#whenever we call ('/' or '/home') then this function will be called.#return render_template("home.html")
    return render_template("home.html")