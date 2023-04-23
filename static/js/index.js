let loggedIn = false;
window.onload = function () {
    let usernameD = document.getElementById("welcome");
    let test = usernameD.getAttribute("data-logged-in");
    if (test === 'True') {
        let loginButtonDiv = loginButton.parentElement;
        //loginButtonDiv.style.display = "none";
        loggedIn = true;
        loginButton.textContent = "Log Out";
    } else if (test === 'False') {
        loggedIn = false;
        loginButton.textContent = "Log In";
    }
};

let loginButton = document.getElementById("userLogin");
loginButton.addEventListener("click", function () {
    if (loggedIn === true) {
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/login", true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.onload = function () {
            if (xhr.status === 200) {
                window.location.href = "/";
            }
        };
        xhr.send('loggedIn=True');
    } else {
        window.location.href = "/login";
    }
});

const productsDiv = document.getElementById("products");
const filterButton = document.getElementById("filterButton");
const filtersSelect = document.getElementById("filters");
const itemsSelect = document.getElementById("items");

filterButton.addEventListener("click", function () {
    const selectedFilter = filtersSelect.value;
    const selectedItem = itemsSelect.value;
    showElements(parseInt(selectedFilter), parseInt(selectedItem));
});
const showElements = function (filter, type) {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/list");
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function () {
        if (xhr.status === 200) {
            productsDiv.innerHTML = "";
            const items = JSON.parse(xhr.responseText);
            createObject(items);
        } else {
            alert(xhr.statusText);
        }
    }
    xhr.send(`item_type=${type}&filter_type=${filter}`);
};

const createObject = function (items){
    items.forEach(item => {
                const itemElement = document.createElement("div");
                const nameElement = document.createElement("h2");
                const descriptionElement = document.createElement("p");
                const priceElement = document.createElement("p");
                const sellerElement = document.createElement("p");
                const imageElement = document.createElement("img");
                const sizeElement = document.createElement("p");
                const colourElement = document.createElement("p");
                const specElement = document.createElement("p");
                const ratingElement = document.createElement("p");
                // form for reviews
                const formElement = document.createElement("form");
                const ratingLabelElement = document.createElement("label");
                const ratingDropdownElement = document.createElement("select");
                const reviewLabelElement = document.createElement("label");
                const reviewTextElement = document.createElement("textarea");
                const reviewSubmitElement = document.createElement("input");

                const reviewsElement = document.createElement("ul");

                item.reviews.forEach(review => {
                    const reviewElement = document.createElement("li");
                    reviewElement.textContent = review.username + ": " + review.inner + " (" + review.rating + " rating)";
                    reviewElement.className = "review";
                    reviewsElement.appendChild(reviewElement);
                });

                itemElement.className = "item";

                nameElement.textContent = item.name;
                nameElement.className = "name";

                descriptionElement.textContent = item.description;
                descriptionElement.className = "description";

                priceElement.textContent = "Price: " + item.price + " " + item.currency;
                priceElement.className = "price"

                sellerElement.textContent = "Seller: " + item.seller;
                sellerElement.className = "seller";

                imageElement.src = item.image;
                imageElement.className = "image";
                imageElement.alt = item.name + " image";

                sizeElement.textContent = "Size: " + item.size;
                sizeElement.className = "size";

                colourElement.textContent = "Colour: " + item.colour;
                colourElement.className = "colour";

                specElement.textContent = "Spec: " + item.spec;
                specElement.className = "spec";

                ratingElement.textContent = "Rating: " + item.rating;
                ratingElement.className = "rating";

                // reviews part
                formElement.setAttribute("id", "reviewForm");
                ratingLabelElement.setAttribute("for", "rating");
                ratingLabelElement.textContent = "Rating:   ";
                ratingDropdownElement.setAttribute("id", "rating");
                ratingDropdownElement.setAttribute("name", "rating");
                for (let i = 1; i <= 5; i++) {
                    const optionElement = document.createElement("option");
                    optionElement.setAttribute("value", i);
                    optionElement.text = i;
                    ratingDropdownElement.appendChild(optionElement);
                }

                reviewLabelElement.setAttribute("for", "review");
                reviewLabelElement.textContent = "Review: ";

                reviewTextElement.setAttribute("id", "review");
                reviewTextElement.setAttribute("name", "review");

                reviewSubmitElement.setAttribute("type", "submit");
                if (loggedIn) {
                    reviewSubmitElement.setAttribute("value", "Submit Review");
                } else {
                    reviewSubmitElement.setAttribute("value", "Login to Submit!");
                }


                reviewsElement.className = "reviews";

                formElement.appendChild(ratingLabelElement);
                formElement.appendChild(ratingDropdownElement);
                formElement.appendChild(reviewLabelElement);
                formElement.appendChild(reviewTextElement);
                formElement.appendChild(reviewSubmitElement);

                itemElement.appendChild(nameElement);
                itemElement.appendChild(descriptionElement);
                itemElement.appendChild(priceElement);
                itemElement.appendChild(sellerElement);
                itemElement.appendChild(imageElement);
                itemElement.appendChild(sizeElement);
                itemElement.appendChild(colourElement);
                itemElement.appendChild(specElement);
                itemElement.appendChild(ratingElement);
                itemElement.appendChild(formElement);
                itemElement.appendChild(reviewsElement);

                itemElement.setAttribute("itemname", item.name);
                productsDiv.appendChild(itemElement);
            })
}

productsDiv.addEventListener("submit", function (e) {
    e.preventDefault();
    if (loggedIn) {
        const reviewForm = e.target;
        const reviewFormInputs = reviewForm.querySelectorAll('input, select, textarea');
        const formValues = {};
        reviewFormInputs.forEach((input) => {
            formValues[input.name] = input.value;
        });

        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/review');
        xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
        xhr.onload = function () {
            const resp = JSON.parse(xhr.responseText);
            const infoElement = document.createElement("p");
            infoElement.textContent = resp.message;
            reviewForm.appendChild(infoElement);
        };
        let selectedItem = itemsSelect.value;
        let itemName = reviewForm.parentElement.getAttribute("itemname");
        xhr.send(`item_name=${itemName}&review=${formValues['review']}&rating=${formValues['rating']}&type=${selectedItem}`);
    } else {
        alert("Please log in to submit review!")
    }
});

