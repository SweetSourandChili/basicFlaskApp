const addUserBtn = document.getElementById("addUser");
const removeUserBtn = document.getElementById("removeUser");
const addItemBtn = document.getElementById("addItem");
const removeItemBtn = document.getElementById("removeItem");

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
        console.log(input.value);
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
    // Do something when the Add Item button is clicked
    // You can add your own code here to handle the form submission
    console.log('Add Item button clicked!');
});

removeItemForm.addEventListener('submit', function (e) {
    e.preventDefault();
    // Do something when the Remove Item button is clicked
    // You can add your own code here to handle the form submission
    console.log('Remove Item button clicked!');
});