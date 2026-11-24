## How the Review List Works

The Review List lets users browse reviews that have already been submitted to EwhaMarket. When a user opens `/review`, Flask calls `DB.get_reviews()` to load the review records. Each record has a review ID and its associated data. The list page uses that ID to link to the individual review.

### Select the reviews for the current page

The route uses two settings to control how many reviews appear on each page and how they are arranged.

```python
reviews = list(DB.get_reviews().items())
per_page = 4
per_row = 2
```

`per_page` limits each page to four reviews. `per_row` tells the route to group the selected reviews into rows of two. These settings control different parts of the display. The first determines which records are included on a page, and the second determines how those records are arranged.

The route reads the `page` query parameter from the URL. For example, `/review?page=2` requests the second page. If there are enough reviews, the route skips the first four and selects the next four.

```python
start = (page - 1) * per_page
page_reviews = reviews[start:start + per_page]
```

For page two, `start` is `4`, so the slice starts at the fifth review. The route then groups the selected records into rows and passes them to the review template. A full page has two rows of two reviews. If the final page has only one review left, the slice returns that one record.

### Open an individual review

When a user selects a review, the browser opens `/view_review_detail/<review_id>`. Flask calls `DB.get_review_by_id(review_id)` and passes the result to `review_detail.html`. The list page gives users a way to browse several entries, and the detail page displays the selected review.

### Review List Result

The screenshot shows a full page of four reviews arranged in a 2×2 grid in the in-class EwhaMarket website.

![EwhaMarket Review List showing four reviews in a 2×2 grid](https://qamarinafazlin.github.io/2026_osp_project_SEAM/assets/images/review-2x2.png)
