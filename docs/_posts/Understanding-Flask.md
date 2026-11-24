---
layout: post
title: "Understanding Flask: How Routes, Sessions, and Jinja2 Templates Work Together in EwhaMarket"
date: 2026-11-24
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
