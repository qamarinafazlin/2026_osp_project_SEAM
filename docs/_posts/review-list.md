---
title: "How the Review List Page Works"
---

## Context

Snack Passport is our team’s web application for browsing snacks and sharing reviews. I worked on the frontend of the Review List page, where users can see what other people thought about different snacks. During development, I used sample reviews to build the page and check how several entries looked together. Each sample included a title, a product name, a rating, and a short description. This gave me enough variety to see how the page handled different amounts of text.

## Goal

My goal was to make it easy for users to scan the reviews and recognize which snack each review was about. I wanted each review to have a clear title and a consistent layout. I also wanted the page to show as many reviews as it received without having to write a separate block of HTML for every entry.

## Steps

### 1. Pass the review data from Flask to the template

When a user opens the Review List, the browser sends a request to `/review`. The Flask route handles that request and renders `review_list.html`. During frontend development, I used a list of sample reviews to check the layout. The route passes the list to the template as `reviews`, so the template can access it while building the page.

### 2. Turn each review into a card

In `review_list.html`, a Jinja `for` loop goes through the list and creates one card per review. The example below shows the main idea with four fields from each entry.

{% raw %}
```html
{% for review in reviews %}
  <article class="review-card">
    <h2>{{ review.title }}</h2>
    <p>{{ review.product_name }} · {{ review.rating }}/5</p>
    <p>{{ review.content }}</p>
  </article>
{% endfor %}
```
{% endraw %}

On each pass through the loop, `review` refers to the current entry. Jinja inserts that entry’s title, product name, rating, and text into the HTML. If Flask passes four reviews, the loop creates four cards. When a review is added to the list, the same template can display the additional card.

### 3. Fit the cards into the shared layout

The review template uses `base.html` for the shared header and navigation. The Review List template provides the content for this particular page, and CSS controls the spacing and appearance of the cards. I could adjust the review layout while using the same navigation as the other Snack Passport pages.

## Result

The Review List displays each review in its own card. A user can scan the titles and ratings first, then read the text of the reviews they are interested in. During development, the sample entries helped me see how longer titles and comments fit into the same card layout.

<!-- Insert the Review List screenshot here. -->
<img width="1316" height="812" alt="image" src="https://github.com/user-attachments/assets/b5b96f8c-31f3-4a16-9583-e2fea3bf5389" />

## References

- Open Software Platform, Lecture 11, *Web Application*
- [Snack Passport project repository](https://github.com/qamarinafazlin/2026_osp_project_SEAM)
