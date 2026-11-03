from flask import Flask, render_template, request
import os

app = Flask(__name__)

# folder where uploaded pictures are saved
UPLOAD_FOLDER = os.path.join("static", "images")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# home page
@app.route("/")
def index():
    return render_template("index.html")


# subpages
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


# product registration (POST from reg_items.html)
@app.route("/result", methods=["POST"])
def reg_item_submit_post():
    data = request.form                     # text inputs
    image_file = request.files["picture"]   # uploaded picture
    filename = image_file.filename
    image_file.save(os.path.join(UPLOAD_FOLDER, filename))
    return render_template("result.html", data=data, img_path="images/" + filename)


# review registration (POST from reg_reviews.html), placeholder for now
@app.route("/submit_review", methods=["POST"])
def reg_review_submit():
    return render_template("review.html")


# temporary user storage (resets when the server restarts; replace with a DB later)
users = {}

@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        user_id = request.form["id"]
        if user_id in users:
            return render_template("signup.html", message="That ID is already taken.")
        users[user_id] = {
            "password": request.form["password"],
            "nickname": request.form["nickname"],
        }
        return render_template("signup.html", message="Account created! You can log in now.")
    return render_template("signup.html")

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form["id"]
        password = request.form["password"]
        user = users.get(user_id)
        if user is None or user["password"] != password:
            return render_template("login.html", message="Wrong ID or password.")
        return render_template("login.html", message="Welcome, " + user["nickname"] + "!")
    return render_template("login.html")

if __name__ == "__main__":
    app.run(debug=True)
