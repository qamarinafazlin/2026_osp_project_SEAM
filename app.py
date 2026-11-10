
from flask import Flask, render_template, request, session, redirect, url_for, flash
from database import DBhandler
import hashlib
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "helloosp"
DB = DBhandler()

UPLOAD_FOLDER = os.path.join("static", "images")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


@app.route("/")
def index():
    return render_template("index.html")

@app.route("/list")
def view_list():
    return render_template("list.html")

@app.route("/review")
def view_review():
    return render_template("review.html")

@app.route("/reg_items")
def reg_item():
    return render_template("reg_items.html")

@app.route("/reg_reviews")
def reg_review():
    return render_template("reg_reviews.html")


# product registration -> saved to Firebase
@app.route("/result", methods=["POST"])
def reg_item_submit_post():
    data = request.form
    image_file = request.files["picture"]
    filename = image_file.filename
    image_file.save(os.path.join(UPLOAD_FOLDER, filename))
    DB.insert_item(data["product_name"], data, filename)
    return render_template("result.html", data=data, img_path="images/" + filename)


@app.route("/submit_review", methods=["POST"])
def reg_review_submit():
    return render_template("review.html")


# sign up -> saved to Firebase under "user", password hashed
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = request.form
        pw_hash = hashlib.sha256(data["password"].encode("utf-8")).hexdigest()
        if DB.insert_user(data, pw_hash):
            return render_template("login.html", message="Account created! Please log in.")
        return render_template("signup.html", message="User ID already exists!")
    return render_template("signup.html")

# Login -> checks Firebase
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form["id"]
        password = request.form["password"]

        pw_hash = hashlib.sha256(
            password.encode("utf-8")
        ).hexdigest()

        user = DB.find_user(user_id, pw_hash)

        if user is None:
            flash("Wrong ID or PW!")
            return redirect(url_for("login"))

        session["id"] = user_id
        return redirect(url_for("index"))

    return render_template("login.html")


# Logout
@app.route("/logout")
def logout():
    session.pop("id", None)
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)
