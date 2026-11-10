from flask import Flask, render_template, request
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
    products = DB.get_items()

    page = request.args.get("page", 1, type=int)
    per_page = 4

    total_pages = max(
        1, (len(products) + per_page - 1) // per_page
    )

    page = max(1, min(page, total_pages))

    start = (page - 1) * per_page
    end = start + per_page

    return render_template(
        "main.html",
        products=products[start:end],
        page=page,
        total_pages=total_pages
    )



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


# login -> checks Firebase
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        pw_hash = hashlib.sha256(request.form["password"].encode("utf-8")).hexdigest()
        user = DB.find_user(request.form["id"], pw_hash)
        if user is None:
            return render_template("login.html", message="Wrong ID or password.")
        return render_template("login.html", message="Welcome, " + user["nickname"] + "!")
    return render_template("login.html")


if __name__ == "__main__":
    app.run(debug=True)
