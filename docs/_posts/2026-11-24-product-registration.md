---
title: "Registering a Product"
---

## Context

EwhaMarket is the website our team built in class for students who want to list snacks. I worked on the frontend of the Product Registration page. This page gives a seller a place to enter information about a product and choose a picture before submitting the listing. The registration process connects an HTML form, a Flask route, and the database.

## Goal

The goal was to let a seller submit the product details and picture in one form and see the submitted information afterward. The form labels help the seller understand what to enter. The input names also matter because the Flask handler uses them to identify the values that arrive from the browser.

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

## What We Learned

I learned how the frontend form and the Flask handler share responsibility for registration. The form's `name` attributes determine how the server finds the submitted values. Looking at the route also helped me understand why an uploaded image and a text field are handled separately, even when the user submits them together.

## References

- [EwhaMarket Flask routes](https://github.com/qamarinafazlin/2026_osp_project_SEAM/blob/main/app.py)
- [Product registration template](https://github.com/qamarinafazlin/2026_osp_project_SEAM/blob/main/templates/reg_items.html)
