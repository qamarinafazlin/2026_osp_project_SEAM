---
title: "Registering a Product and Review Lists"
---
## Context

EwhaMarket is the website our team built in class for students who want to list snacks and share reviews. In this post, we explain how a seller submits a product listing and how EwhaMarket displays existing reviews. The registration form sends new product details and a picture to Flask, while the Review List loads saved reviews for users to browse.

## Goal

The Product Registration page lets sellers submit listing details and a picture in one form and see the result after submitting it. The Review List helps users browse existing reviews by showing up to four at a time and linking each entry to its detail page.

## Steps

### 1. Open the registration form

The registration page is available at `/reg_items`. When a user opens this address, Flask renders the `reg_items.html` template.

```python
@app.route("/reg_items")
def reg_item():
    return render_template("reg_items.html")
```

This route handles opening the form. Once the form appears, the user can fill in the product details and select a picture. Submitting the form sends a separate `POST` request to `/result`.

### 2. Read and save the submitted information

The `/result` handler reads the text fields and the picture from different parts of the request. The following lines show how the handler receives those values and saves the listing.

```python
data = request.form
image_file = request.files["picture"]
filename = image_file.filename
image_file.save(os.path.join(UPLOAD_FOLDER, filename))
DB.insert_item(data["product_name"], data, filename)
```

`request.form` contains the submitted text values. `request.files["picture"]` gives Flask the uploaded image file. The handler saves the image to the server's upload folder, then passes the product name, form data, and image filename to `DB.insert_item()` to store the listing in Firebase.

### 3. Display the result

After saving the listing, Flask renders the result template with the submitted values and the path to the uploaded image.

```python
return render_template(
    "result.html",
    data=data,
    img_path="images/" + filename
)
```

The `data` argument gives the template access to the submitted text. The `img_path` argument tells the template where to find the picture. This gives the seller a result page where they can see the information they just entered.

## Result

The registration flow starts with the product form and ends with a page showing the submitted listing details and picture. For example, a seller can enter a snack's name and price, choose a photo, and check those details on the result page after submitting the form.
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

## What We Learned

We learned how HTML field names connect the registration form to the Flask handler and why Flask reads text fields and uploaded pictures separately. We also learned how pagination and layout work together. The Flask route selects up to four reviews for the current page and groups them into rows of two before passing them to the template.

## References

- [EwhaMarket Flask routes](https://github.com/qamarinafazlin/2026_osp_project_SEAM/blob/main/app.py)
- [Product registration template](https://github.com/qamarinafazlin/2026_osp_project_SEAM/blob/main/templates/reg_items.html)
