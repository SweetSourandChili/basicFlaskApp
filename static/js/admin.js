const addUserForm = document.getElementById('addUserForm');
const addUserInputs = addUserForm.querySelectorAll('input, select, textarea');

const removeUserForm = document.getElementById('removeUserForm');
const removeUserInputs = removeUserForm.querySelectorAll('input, select, textarea');

const addItemForm = document.getElementById('addItemForm');
const addItemInputs = addItemForm.querySelectorAll('input, select, textarea');

const removeItemForm = document.getElementById('removeItemForm');
const removeItemInputs = removeItemForm.querySelectorAll('input, select, textarea');
addUserForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const formValues = {};
    addUserInputs.forEach((input) => {
        formValues[input.name] = input.value;
    });
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/user');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function () {
        const resp = JSON.parse(xhr.responseText);
        addUserForm.querySelector("p").textContent = resp.message;
    };
    xhr.send(`username=${formValues['username']}&password=${formValues['password']}&add=True`);
});

removeUserForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const formValues = {};
    removeUserInputs.forEach((input) => {
        formValues[input.name] = input.value;
    });
    console.log(formValues);
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/user');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function () {
        const resp = JSON.parse(xhr.responseText);
        removeUserForm.querySelector("p").textContent = resp.message;
    };
    xhr.send(`username=${formValues['username']}&add=False`);
});

addItemForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const formValues = {};
    addItemInputs.forEach((input) => {
        formValues[input.name] = input.value;
    });
    const xhr = new XMLHttpRequest();
    xhr.open('POST', '/item');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function () {
        const resp = JSON.parse(xhr.responseText);
        addItemForm.querySelector("p").textContent = resp.message;
    };
    xhr.send(`&name=${formValues['name']}&description=${formValues['description']}&price=${formValues['price']}&seller=${formValues['seller']}&image_link=${formValues['image_link']}&size=${formValues['size']}&colour=${formValues['colour']}&spec=${formValues['spec']}&item_type=${formValues['item_type']}&add=True`);
});

removeItemForm.addEventListener('submit', function (e) {
    e.preventDefault();
    const formValues = {};
    removeItemInputs.forEach((input) =>{
       formValues[input.name] = input.value;
    });
    const xhr = new XMLHttpRequest();
    xhr.open('POST','/item');
    xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
    xhr.onload = function (){
        const resp = JSON.parse(xhr.responseText);
        removeItemForm.querySelector("p").textContent = resp.message;
    }
    xhr.send(`&name=${formValues['name']}&item_type=${formValues['item_type']}&add=False`);


});