---
layout: post
title: "Explanation: How the Like Button Works"
date: 2026-11-24
---

**Category:** Explanation  
**Project:** EwhaMarket  
**Team:** SEAM  
**Technologies:** Python, Flask, JavaScript, JSON, Firebase Realtime Database

## Context

The **product detail page** is the most important page in EwhaMarket. It is where a buyer sees a snack's photo, price, seller and pickup address, and decides whether to buy it.

On this page we added a **Like** button. Logged-in users can click it to save snacks they are interested in, and click it again to undo. What makes this feature different from the rest of our website is that it uses **AJAX**: clicking the button saves the like to Firebase **without reloading the page**.

| Before clicking | After clicking |
|---|---|
| ![Product detail page with an empty Like button]({{ "/assets/images/like-before.png" | relative_url }}) | ![Product detail page with a red Liked button]({{ "/assets/images/like-after.png" | relative_url }}) |

## Goal

- Show **♡ Like** or **♥ Liked** depending on what the user saved before
- Switch between the two states when the button is clicked
- Save each user's like separately in Firebase
- Update **only the button**, not the whole page
- Show a clear message if the user is not logged in

## Why AJAX?

The other forms on our website, like product registration and login, send the data and then load a **whole new page**. For a Like button, that would feel slow: the page would flash, scroll back to the top and download the images again just to change one heart.

With AJAX, the browser and the server exchange only a small piece of data:

| | Normal form | AJAX (our Like button) |
|---|---|---|
| What the browser sends | Form data | JSON: `{"liked": true}` |
| What the server sends back | A full HTML page | JSON: `{"liked": true}` |
| What changes on screen | The whole page | Only the button |
| Flask function | `render_template()` | `jsonify()` |

## How It Works

There are three parts: **the database**, **the Flask route**, and **the JavaScript** in `detail.html`.

```text
Browser (detail.html)           Flask (app.py)                 Firebase
────────────────────           ──────────────                 ────────
page opens
  fetch GET  ───────────────►   /item_like/durian
                                  DB.get_heart()  ───────────►  heart/nina/durian
  show ♡ or ♥ ◄──────────────    jsonify({"liked": ...})
click
  fetch POST {"liked": true} ►  /item_like/durian
                                  DB.set_heart()  ───────────►  saved
  show ♥     ◄──────────────    jsonify({"liked": true})
```

### 1. Store likes per user in Firebase

Each like is saved under the user's ID and the product name, so two users can like the same snack without affecting each other.

```text
heart
 └── nina
      └── durian
           └── liked: true
```

In `database.py`, we added two functions: one to read a like and one to save it.

```python
def get_heart(self, user_id, name):
    heart = self.db.child("heart").child(user_id).child(name).get().val()
    if heart is None:          # this user never clicked Like on this product
        return False
    return heart.get("liked", False)

def set_heart(self, user_id, name, liked):
    self.db.child("heart").child(user_id).child(name).set({"liked": bool(liked)})
    return bool(liked)
```

We used `set()` instead of `push()` because each user should have **only one** like per product. `set()` overwrites the old value, while `push()` would add a new entry every time.

### 2. Answer with JSON in Flask

One route handles both reading and saving. `GET` returns the current state, and `POST` saves a new state. Both return JSON with `jsonify()` instead of a page.

```python
from flask import jsonify

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
```

The user's ID comes from the **session**, which is set when they log in. If nobody is logged in, the route returns status code **401 (Unauthorized)**, so the browser knows to show a login message instead of a heart.

Data sent from JavaScript as JSON is read with `request.get_json()`. Our other forms use `request.form`, because they send HTML form data instead of JSON.

### 3. Update the button with JavaScript

The script at the bottom of `detail.html` does two jobs: it loads the saved state when the page opens, and it saves a new state when the button is clicked.

{% raw %}
```javascript
const button = document.getElementById("like-button");
const message = document.getElementById("like-message");
const likeUrl = "/item_like/" + encodeURIComponent({{ name | tojson }});
let liked = false;

function showLikeState(value) {
    liked = value;
    button.textContent = liked ? "♥ Liked" : "♡ Like";
    button.style.color = liked ? "red" : "black";
}
```
{% endraw %}

{% raw %}`{{ name | tojson }}`{% endraw %} puts the product name from Flask into JavaScript safely, and `encodeURIComponent()` makes names with spaces (like `Khao Soi`) work in the URL.

**When the page opens**, the script asks the server for the saved state:

```javascript
async function loadLikeState() {
    try {
        const response = await fetch(likeUrl);          // GET
        if (response.status === 401) {
            throw new Error("Please log in to use likes.");
        }
        const data = await response.json();
        showLikeState(data.liked);
        button.disabled = false;
    } catch (error) {
        button.textContent = "Like unavailable";
        message.textContent = error.message;
    }
}
```

**When the button is clicked**, it sends the opposite of the current state:

```javascript
button.addEventListener("click", async function () {
    const nextState = !liked;
    button.disabled = true;                              // stop double clicks
    try {
        const response = await fetch(likeUrl, {
            method: "POST",
            headers: { "Content-Type": "application/json" },
            body: JSON.stringify({ liked: nextState })
        });
        if (!response.ok) {
            throw new Error("Could not save your like. Please log in again.");
        }
        const data = await response.json();
        showLikeState(data.liked);
    } catch (error) {
        message.textContent = error.message;
    } finally {
        button.disabled = false;
    }
});
```

A few details we were careful about:

- **`await`** makes the code wait for the server's answer before reading it. `async` is needed on the function so `await` can be used inside it.
- **The button changes only after the server answers.** We show what Firebase actually saved (`data.liked`), not what we hoped it saved, so the button never shows a like that wasn't stored.
- **The button is disabled while waiting.** Without this, clicking twice quickly could send two requests and leave the button in the wrong state.
- **`finally`** turns the button back on whether the request worked or failed.

## Result

| Situation | What the user sees |
|---|---|
| Not logged in | "Like unavailable" and the message "Please log in to use likes." |
| Logged in, never liked | ♡ Like |
| Click | ♥ Liked (red), saved in Firebase, no page reload |
| Click again | ♡ Like |
| Refresh the page or come back later | The saved state is shown again |
| Another user opens the same product | Their own like state, not ours |

The Like button is a small feature, but it connects every part of our website: **HTML** for the button, **JavaScript** for the request, **Flask** for checking the session and answering with JSON, and **Firebase** for storing each user's choice.

## References

- Open Software Platform, Lecture 10, *Web Application (2)*: AJAX, `fetch()`, `jsonify()`, `request.get_json()'
- [EwhaMarket project repository](https://github.com/qamarinafazlin/2026_osp_project_SEAM)
