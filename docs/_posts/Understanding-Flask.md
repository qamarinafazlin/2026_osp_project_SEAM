---
title: "Understanding Flask: How Routes, Sessions, and Jinja2 Templates Work Together in EwhaMarket"
---

## Context
While building the **EwhaMarket** web application in `2026_osp_project_SEAM`, I used **Flask** (`app.py`) together with HTML templates (`templates/`) to handle navigation, product and review pages, form submissions, and user login state. Because HTTP requests are stateless by default, I wanted a clear understanding of how Flask connects URLs to Python functions, passes context into templates, and remembers who is logged in across pages.

## Problem or Goal
When a web app has separate pages for viewing products (`/list`), opening product details (`/view_detail/<name>`), logging in (`/login`), and liking items (`/toggle_like/<name>`), it is easy to lose track of how data moves between the server and the browser. The goal of this post is to explain three core Flask concepts—**routing (including dynamic URLs)**, **template rendering with Jinja2**, and **user sessions (`session`)**—using real examples from `app.py` and our templates.

## Steps

### 1. Static and Dynamic Routes (`@app.route`)
In `app.py`, `@app.route(...)` maps URLs to Python view functions. Some routes use fixed paths like `/list` or `/reg_reviews`, while others use angle brackets like `<name>` or `<review_id>` to capture dynamic values straight from the URL.

```python
# product detail (dynamic routing)
@app.route("/view_detail/<name>")
def view_item_detail(name):
    data = DB.get_item_byname(str(name))
    return render_template("detail.html", name=name, data=data)


# /reg_reviews?name=apple -> product name is filled in
@app.route("/reg_reviews")
def reg_review():
    name = request.args.get("name", "")
    return render_template("reg_reviews.html", name=name)

```

In `view_item_detail(name)`, Flask passes `<name>` from the URL as a function argument so we can fetch that item from the database. In `reg_review()`, `request.args.get("name", "")` reads an optional query parameter so clicking "Write a review" on a product detail page can pre-fill the product name in `reg_reviews.html`.

### 2. Template Inheritance and `render_template()`
Instead of repeating the navigation bar on every page, `index.html` defines a shared layout with `{% block section %}`, and child templates like `list.html`, `detail.html`, and `login.html` extend it using `{% extends "index.html" %}`. When `app.py` calls `render_template(...)`, Flask renders the template on the server and fills in the variables passed to it.

```html
<nav class="pagination">
    {% if page_arg > 1 %}
    <a href="{{ url_for('view_list', page=page_arg - 1) }}">Prev</a>
    {% endif %}

    {% for p in range(1, total_pages + 1) %}
        {% if p == page_arg %}
        <b>{{ p }}</b>
        {% else %}
        <a href="{{ url_for('view_list', page=p) }}">{{ p }}</a>
        {% endif %}
    {% endfor %}
</nav>
```

In `list.html`, `page_arg` and `total_pages` come from `view_list()` in `app.py`, and `url_for('view_list', page=p)` dynamically generates pagination links pointing back to the `view_list` route.

### 3. Remembering Users with `session` and `SECRET_KEY`
In `app.py`, `app.config["SECRET_KEY"] = "helloosp"` enables Flask's signed session cookie (`session`), allowing the app to remember a logged-in user across requests.

```python
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
```

Once `session["id"]` is set on login, `index.html` can display `Hello, {{ session["id"] }}!` and a logout link, `detail.html` can check whether `session.get("id")` already liked an item, `/toggle_like/<name>` can require a logged-in user, and `/logout` can clear the session with `session.clear()`.

## Result
<img width="1100" height="760" alt="detail-not-liked" src="https://github.com/user-attachments/assets/39c25857-2bd1-4c2b-9ab3-0351ee5ea97f" />

Together, `@app.route()`, `request.args` / `request.form`, `render_template()` with `url_for()`, and `session` let EwhaMarket serve multi-page views, pass data cleanly between routes and HTML templates, and keep user login state across pages.

## What I Learned
Working on `app.py` and the HTML templates showed me how clean a Flask app becomes when you separate URL routing, database access (`DBhandler`), and Jinja2 presentation. I also learned how `url_for()` keeps links tied to function names rather than hard-coded strings, and how `session` bridges the gap between logging in once and using features like liking items or submitting reviews.

## References
* Flask Documentation: [Routing](https://flask.palletsprojects.com/en/stable/quickstart/#routing), [Rendering Templates](https://flask.palletsprojects.com/en/stable/quickstart/#rendering-templates), and [Sessions](https://flask.palletsprojects.com/en/stable/quickstart/#sessions)
