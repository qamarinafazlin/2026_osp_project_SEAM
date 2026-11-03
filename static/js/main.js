// Runs after the page has loaded (because of "defer")

// 1) Highlight the current page in the nav bar
const links = document.querySelectorAll(".navbar__menu a");
links.forEach(function (link) {
    if (link.getAttribute("href") === window.location.pathname) {
        link.classList.add("active");
    }
});

// 2) Product registration form (only on /reg_items)
const itemForm = document.querySelector('form[action="/result"]');
if (itemForm) {
    // Show a preview of the picture before submitting
    const fileInput = itemForm.querySelector('input[name="picture"]');
    const preview = document.createElement("img");
    preview.width = 200;
    preview.style.display = "none";
    fileInput.after(preview);

    fileInput.addEventListener("change", function () {
        const file = fileInput.files[0];
        if (file) {
            preview.src = URL.createObjectURL(file);
            preview.style.display = "block";
        }
    });

    // Check the price and ask for confirmation before submitting
    itemForm.addEventListener("submit", function (event) {
        const price = Number(itemForm.querySelector('input[name="price"]').value);
        if (price <= 0) {
            alert("Price must be more than 0!");
            event.preventDefault();   // stop the submit
            return;
        }
        if (!confirm("Register this product?")) {
            event.preventDefault();
        }
    });
}

// 3) Review form (only on /reg_reviews)
const reviewForm = document.querySelector('form[action="/submit_review"]');
if (reviewForm) {
    reviewForm.addEventListener("submit", function () {
        alert("Thanks for your review!");
    });
}