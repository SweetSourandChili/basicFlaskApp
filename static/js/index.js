var loggedIn = false;
window.onload = function() {
    let usernameD = document.getElementById("welcome");
    let test = usernameD.getAttribute("data-logged-in");
    if (test === 'True') {
        let loginButtonDiv = loginButton.parentElement;
        //loginButtonDiv.style.display = "none";
        loggedIn = true;
        loginButton.textContent = "Log Out";
    } else if (test === 'False'){
        loggedIn = false;
        loginButton.textContent = "Log In";
    }
};

let loginButton = document.getElementById("userLogin");
loginButton.addEventListener("click", function (){
    if(loggedIn === true){
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/login", true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.onload = function() {
            if (xhr.status === 200) {
                window.location.href = "/";
            }
        };
        xhr.send('loggedIn=True');
    }
    else{
        window.location.href = "/login";
    }
});

const productsDiv = document.getElementById("products");
const filterButton = document.getElementById("filterButton");
const filtersSelect = document.getElementById("filters");
const itemsSelect = document.getElementById("items");

filterButton.addEventListener("click", function() {
    const selectedFilter = filtersSelect.value;
    const selectedItem = itemsSelect.value;
    showElements(parseInt(selectedItem));
});
const showElements = function (type) {
    const xhr = new XMLHttpRequest();
    xhr.open("POST", "/list");
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function() {
        if (xhr.status === 200) {
            productsDiv.innerHTML = "";
            const items = JSON.parse(xhr.responseText);
            items.forEach(item =>{
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
                const reviewsElement = document.createElement("ul");

                item.reviews.forEach(review => {
                const reviewElement = document.createElement("li");
                reviewElement.textContent = review.username + ": " + review.comment + " (" + review.rating + " stars)";
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

                reviewsElement.className = "reviews";


                itemElement.appendChild(nameElement);
                itemElement.appendChild(descriptionElement);
                itemElement.appendChild(priceElement);
                itemElement.appendChild(sellerElement);
                itemElement.appendChild(imageElement);
                itemElement.appendChild(sizeElement);
                itemElement.appendChild(colourElement);
                itemElement.appendChild(specElement);
                itemElement.appendChild(ratingElement);
                itemElement.appendChild(reviewsElement);

                productsDiv.appendChild(itemElement);
            })
        }
        else{
            alert(xhr.statusText);
        }
    }
    xhr.send(`item_type=${type}`);
};
