from flask import Flask, render_template, request, session, redirect, url_for, flash, jsonify
from database import DBhandler
import hashlib
import os

app = Flask(__name__)
app.config["SECRET_KEY"] = "helloosp"
DB = DBhandler()

UPLOAD_FOLDER = os.path.join("static", "images")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


# ---------- main ----------
@app.route("/")
def index():
    return render_template("index.html")


# ---------- products ----------
# product list with pagination
@app.route("/list")
def view_list():
    items = DB.get_items()          # list of product dicts
    per_page = 6
    per_row = 3

    page = request.args.get("page", 1, type=int)
    total_pages = max(1, (len(items) + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))

    start = (page - 1) * per_page
    page_items = items[start:start + per_page]

    rows = []
    for i in range(0, len(page_items), per_row):
        rows.append(page_items[i:i + per_row])

    return render_template("list.html", rows=rows,
                           page_arg=page, total_pages=total_pages,
                           total=len(items))


# product detail (dynamic routing)
@app.route("/view_detail/<name>")
def view_item_detail(name):
    data = DB.get_item_byname(str(name))
    return render_template("detail.html", name=name, data=data)

# like (AJAX): GET = load state, POST = save new state
@app.route("/item_like/<name>", methods=["GET", "POST"])
def item_like(name):
    user_id = session.get("id")
    if user_id is None:
        return jsonify({"error": "Login required"}), 401

    if request.method == "GET":
        return jsonify({"liked": DB.get_heart(user_id, name)})

    data = request.get_json()
    saved = DB.set_heart(user_id, name, data["liked"])
    return jsonify({"liked": saved})
@app.route("/reg_items")
def reg_item():
    return render_template("reg_items.html")


# product registration -> saved to Firebase
@app.route("/result", methods=["POST"])
def reg_item_submit_post():
    data = request.form
    image_file = request.files["picture"]
    filename = image_file.filename
    image_file.save(os.path.join(UPLOAD_FOLDER, filename))
    DB.insert_item(data["product_name"], data, filename)
    return render_template("result.html", data=data, img_path="images/" + filename)


# ---------- reviews ----------
# review list with pagination (2*2 = 4 per page)
@app.route("/review")
def view_review():
    reviews = list(DB.get_reviews().items())   # [(review_id, review), ...]
    per_page = 4
    per_row = 2

    page = request.args.get("page", 1, type=int)
    total_pages = max(1, (len(reviews) + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))

    start = (page - 1) * per_page
    page_reviews = reviews[start:start + per_page]

    rows = []
    for i in range(0, len(page_reviews), per_row):
        rows.append(page_reviews[i:i + per_row])

    return render_template("review.html", rows=rows,
                           page_arg=page, total_pages=total_pages,
                           total=len(reviews))


# review detail (dynamic routing with the auto-generated key)
@app.route("/view_review_detail/<review_id>")
def view_review_detail(review_id):
    review = DB.get_review_by_id(review_id)
    return render_template("review_detail.html",
                           review_id=review_id, review=review)


# review writing page
# /reg_reviews?name=apple -> product name is filled in
@app.route("/reg_reviews")
def reg_review():
    name = request.args.get("name", "")
    return render_template("reg_reviews.html", name=name)


# review registration -> photo saved on server, review pushed to Firebase
@app.route("/submit_review_post", methods=["POST"])
def reg_review_submit_post():
    data = request.form
    image_file = request.files["photo"]
    filename = image_file.filename
    image_file.save(os.path.join(UPLOAD_FOLDER, filename))
    DB.insert_review(data, filename, session.get("id", "guest"))
    flash("Review registered!")
    return redirect(url_for("view_review"))


# ---------- users ----------
# sign up -> saved to Firebase under "user", password hashed
@app.route("/signup", methods=["GET", "POST"])
def signup():
    if request.method == "POST":
        data = request.form
        pw_hash = hashlib.sha256(data["password"].encode("utf-8")).hexdigest()
        if DB.insert_user(data, pw_hash):
            flash("Account created! Please log in.")
            return redirect(url_for("login"))
        return render_template("signup.html", message="User ID already exists!")
    return render_template("signup.html")


# login -> checks Firebase, remembers the user in the session
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user_id = request.form["id"]
        pw_hash = hashlib.sha256(request.form["password"].encode("utf-8")).hexdigest()
        user = DB.find_user(user_id, pw_hash)

        if user is None:
            flash("Wrong ID or PW!")
            return redirect(url_for("login"))

        session["id"] = user_id
        return redirect(url_for("index"))

    return render_template("login.html")


# logout -> clear session, back to main page
@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("index"))


if __name__ == "__main__":
    app.run(debug=True)