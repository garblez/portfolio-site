from flask import Flask, render_template, request, redirect, url_for

import secrets 


app = Flask(__name__)


def save_paste(paste):
    paste_id = secrets.token_hex(16)
    with open("paste/{}".format(paste_id), "w") as f:
        f.write(paste)
    return paste_id


def get_paste(paste_id=None):
    try:
        with open("paste/{}".format(paste_id), "r") as f:
            paste = f.read()
        return paste
    except FileNotFoundError:
        return None


@app.route("/")
def index():
    return redirect(url_for("paste"))


@app.route("/paste/", methods=["GET", "POST"])
@app.route("/paste/<paste_id>")
def paste(paste_id=None):
    if request.method == "POST":
        # Save the paste in the form to a file
        paste_id = save_paste(request.form["paste"])
        return redirect(url_for("paste") + paste_id)
    paste = get_paste(paste_id)
    return render_template("paste.html", paste_id=paste_id, paste=paste)


@app.errorhandler(404)
def page_not_found(error):
    return render_template("page_not_found.html"), 404
