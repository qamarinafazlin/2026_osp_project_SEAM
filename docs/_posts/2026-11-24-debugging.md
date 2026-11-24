---
layout: post
title: "Debugging our website"
date: 2026-11-24
---

**Category:** Debugging  
**Project:** EwhaMarket  
**Team:** SEAM  
**Technologies:** Python, Flask, Jinja2, HTML

## Context

In EwhaMarket, users can write reviews for the snacks they bought. For our Web Application Practice 2, the review list page had to show each review's title and photo in a **2×2 grid**, with **4 reviews per page** and pagination for the rest.

We set `per_page = 4` in the Flask route and wrote a loop in `review.html`. The page loaded with no errors, the pagination worked, and each page had exactly 4 reviews. But they were all in **one long row**.

## Problem

Instead of two rows of two, the page showed one row of four:

![Review list showing 4 reviews in one row]({{ "/assets/images/review-1x4.png" | relative_url }})

Flask didn't show any error message, so at first we didn't know if the problem was in the CSS, the template, or the route.

## Root Cause

We checked the generated HTML with the browser's developer tools (`F12` → **Elements**). The table had only **one `<tr>`**, and all four `<td>` cells were inside it.

This was our template:

{% raw %}
```html
<table class="item-table">
    <tr>
        {% for review_id, review in reviews %}
        <td class="item-card">
            <img src="/static/images/{{ review.img_path }}">
            <p class="item-name">{{ review.title }}</p>
        </td>
        {% endfor %}
    </tr>
</table>
```
{% endraw %}

And this was the route:

```python
page_reviews = reviews[start:start + per_page]
return render_template("review.html", reviews=page_reviews, ...)
```

There were two connected mistakes:

1. **`per_page = 4` controls how many reviews are on a page, not how they are laid out.** Slicing the list gave us 4 reviews, but it was still one flat list: `[r1, r2, r3, r4]`.
2. **The `<tr>` was outside the loop.** In an HTML table, every `<td>` inside the same `<tr>` sits next to each other horizontally. Since the loop only repeated the `<td>`, all four cells ended up in the same row.

Nothing in our code ever said "start a new row after 2 reviews", so the browser did exactly what the HTML told it to do.

## Solution

We split the page's reviews into rows of 2 **in the Flask route**, so the template receives a list of rows instead of one flat list.

```python
@app.route("/review")
def view_review():
    reviews = list(DB.get_reviews().items())   # [(review_id, review), ...]
    per_page = 4    # how many reviews on one page
    per_row = 2     # how many reviews in one row

    page = request.args.get("page", 1, type=int)
    total_pages = max(1, (len(reviews) + per_page - 1) // per_page)
    page = max(1, min(page, total_pages))

    start = (page - 1) * per_page
    page_reviews = reviews[start:start + per_page]

    # [r1, r2, r3, r4]  ->  [[r1, r2], [r3, r4]]
    rows = []
    for i in range(0, len(page_reviews), per_row):
        rows.append(page_reviews[i:i + per_row])

    return render_template("review.html", rows=rows,
                           page_arg=page, total_pages=total_pages,
                           total=len(reviews))
```

Then we changed the template to use **two loops**. The outer loop creates one `<tr>` per row, and the inner loop creates the `<td>` cells inside it:

{% raw %}
```html
<table class="item-table">
    {% for row in rows %}
    <tr>
        {% for review_id, review in row %}
        <td class="item-card"
            onclick="location.href='/view_review_detail/{{ review_id }}'">
            <img src="/static/images/{{ review.img_path }}" alt="{{ review.title }}">
            <p class="item-name">{{ review.title }}</p>
            <p class="item-price">{{ review.product_name }}</p>
        </td>
        {% endfor %}
    </tr>
    {% endfor %}
</table>
```
{% endraw %}

We chose to fix it in the route and template instead of in CSS. Our product list page uses the same `item-table` class with **3** items per row, so changing the CSS for the table would have broken the product list.

## Result

The review list now shows a proper 2×2 grid. If the last page only has 1 review, the last row simply has 1 cell.

![Review list showing a 2×2 grid]({{ "/assets/images/review-2x2.png" | relative_url }})

| | Before | After |
|---|---|---|
| Data sent to the template | `[r1, r2, r3, r4]` | `[[r1, r2], [r3, r4]]` |
| `<tr>` in the HTML | 1 | 2 |
| Layout | 1×4 | 2×2 |

