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


if __name__ == "__main__":
    app.run(debug=True)
