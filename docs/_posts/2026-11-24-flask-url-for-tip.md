---
title: "Flask Development Tip: Using url_for() Instead of Hardcoded URLs"
date: 2026-11-24
---

**Category:** Tip  
**Project:** EwhaMarket  
**Team:** SEAM  
**Technologies:** Python, Flask, HTML, Jinja2

## 1. Introduction

During the development of EwhaMarket, our team implemented several connected web pages, including a product list, product details, user authentication, and a review registration system. As the number of pages increased, managing navigation links and static resources became an important part of maintaining our application.

One useful development technique is using Flask's built-in `url_for()` function instead of manually writing fixed URL paths. This technique can improve code maintainability and reduce potential navigation errors.

## 2. The Problem with Hardcoded URLs

In our `index.html` template, some navigation links are written using hardcoded URLs.

```html
<li><a href="/list">List</a></li>
<li><a href="/review">Review</a></li>
```

Although these links work with our current Flask routes, they depend directly on the URL paths defined in `app.py`. If a developer changes the product list route from `/list` to `/products`, every hardcoded link pointing to `/list` must also be updated.

A more maintainable alternative is:

{% raw %}
```html
<li><a href="{{ url_for('view_list') }}">List</a></li>
<li><a href="{{ url_for('view_review') }}">Review</a></li>
```
{% endraw %}

Instead of using fixed paths, these links refer to Flask endpoint names. As long as the endpoint names remain unchanged, Flask automatically generates the corresponding URLs.

## 3. Loading Static Resources

Our project already uses `url_for()` to load CSS and JavaScript files in `index.html`.

{% raw %}
```html
<link rel="stylesheet"
      href="{{ url_for('static', filename='css/style.css') }}">

<script src="{{ url_for('static', filename='js/main.js') }}"
        defer></script>
```
{% endraw %}

The `static` endpoint allows Flask to generate URLs for files stored inside the static directory.

Since other HTML templates inherit from `index.html`, these resources can be shared across multiple pages without repeatedly defining them. This helps maintain a consistent design throughout the application.

## 4. Passing Product Information Between Pages

Another practical example appears in our `detail.html` file.

When a user clicks the Write a review button, the application opens the review registration page and passes the selected product name.

{% raw %}
```html
<button type="button" class="review-btn"
        onclick="location.href='{{ url_for('reg_review', name=name) }}'">
    Write a review
</button>
```
{% endraw %}

The corresponding Flask route in `app.py` receives the product name.

```python
@app.route("/reg_reviews")
def reg_review():
    name = request.args.get("name", "")
    return render_template("reg_reviews.html", name=name)
```

For example, if the selected product is Apple, Flask generates a URL such as:

```text
/reg_reviews?name=Apple
```

The server retrieves the product name from the query string using `request.args.get()` and passes it to the review registration template.

This allows product information to be transferred between pages without requiring the user to manually enter the product name again, provided that the form displays the supplied value.

## 5. Redirecting Users After Form Submission

Our project also uses `url_for()` when redirecting users after registering a review.

```python
flash("Review registered!")
return redirect(url_for("view_review"))
```

After the review registration operation, Flask redirects the user to the review list page.

Using `url_for()` here avoids hardcoding the destination URL and helps maintain consistent navigation between different features of the application.

## 6. Result and Benefits

Our current implementation demonstrates several practical uses of `url_for()`:

- Loading CSS and JavaScript files.
- Generating navigation URLs.
- Passing product information through query parameters.
- Redirecting users after form submission.

Using this function makes the application easier to maintain, particularly when multiple team members work on different pages.

However, developers must ensure that endpoint names and required parameters are correct. An incorrect endpoint name can cause a URL building error.

Replacing the remaining hardcoded navigation links would further improve the consistency of our application.

## 7. What I Learned

Through this project, I learned that small development techniques can make a significant difference in code organization.

Using `url_for()` helps separate navigation logic from fixed URL paths and reduces unnecessary dependencies between HTML templates and Flask routes.

This is a useful practice for beginners developing Flask applications, especially when working collaboratively on a website with multiple connected features.

## References

- [Flask Documentation - URL Building](https://flask.palletsprojects.com/en/stable/quickstart/#url-building)
- [Flask Documentation - Static Files](https://flask.palletsprojects.com/en/stable/quickstart/#static-files)
