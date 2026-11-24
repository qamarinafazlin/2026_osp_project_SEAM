---
title: Registering a Product
---

# How Product Registration Works in Snack Passport

## Context

Snack Passport is a team web project where users can list snacks and share reviews. I worked on the frontend of the Product Registration page. This page is where a user enters the information that other people need to understand a listing, such as the snack’s name, price, and availability. The challenge was to organize those details into a form that users could fill out easily and that the Flask backend could process.

## Goal

The goal was to let users enter the details for a snack listing and submit them through one form. The page needed to show what each field was for and keep the same header and navigation as the rest of Snack Passport. It also needed to handle both written information and a product image.

## Steps

### 1. Open the registration page

When the user opens `/reg_items`, Flask renders the `register_product.html` template. The template uses the shared page layout for the header and navigation. The registration form itself belongs to the page-specific template. This structure lets us change the fields or the form layout without editing the navigation on every page.

### 2. Fill in the product details

The form groups information about the snack and the seller. For example, the product name identifies the snack, the price tells other users how much it costs, and the status shows whether it is available. The email field provides a way to contact the seller. The photo field lets the seller add an image so other users can recognize the product.

Each input needs a label for the user and a `name` attribute for the server. The following simplified example shows how a form can send a product name and a photo together.

```html
<form method="post" enctype="multipart/form-data">
  <label for="product-name">Product name</label>
  <input id="product-name" name="name" type="text" required>

  <label for="product-photo">Product photo</label>
  <input id="product-photo" name="photo" type="file" accept="image/*">

  <button type="submit">Register product</button>
</form>
```

The `for` attribute connects each label to its input. The browser uses `method="post"` to submit the form, and `multipart/form-data` lets it include the selected image in the same request as the text fields.

### 3. Send the form to Flask

When the user clicks **Register product**, the browser sends the form to the server. In Flask, the submission handler can read text fields through `request.form` and uploaded files through `request.files`. It identifies each value by the input’s `name` rather than the label the user sees. For example, a field named `photo` must be retrieved using that same name. Matching those names is especially important when different team members work on the template and the Python handler.

## Result

The Product Registration page provides a single form for entering product and seller details and choosing a photo. The labels guide users through the form, and the submit button marks the final step.

<!-- Add a screenshot of the Product Registration page here. -->
<img width="1307" height="803" alt="image" src="https://github.com/user-attachments/assets/45547ac8-d48b-4112-a793-f548455ce126" />

information, and the Flask handler needs to read that information using the same field names. Working on this page helped me understand how a frontend template and a backend route work together during form submission.

## References

- Open Software Platform, Lecture 11, *Web Application*
- [Snack Passport project repository](https://github.com/qamarinafazlin/2026_osp_project_SEAM)
