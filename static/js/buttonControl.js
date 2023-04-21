
let userLogin = document.getElementById("userLogin");
let adminLogin = document.getElementById("adminLogin");
let signIn = document.getElementById("signIn");
let userTable = document.getElementById("userLoginTable");
let adminTable = document.getElementById("adminLoginTable");
let getUser = document.getElementById("readUser");
let getAdmin = document.getElementById("readAdmin");

userLogin.addEventListener("click", function() {
     userTable.style.display = "table";
     adminTable.style.display = "none";
});

adminLogin.addEventListener("click", function() {
     userTable.style.display = "none";
     adminTable.style.display = "table";
});

getUser.addEventListener("click", function() {
     let inp = document.getElementsByTagName("input");
     const username = inp[0].value;
     const password = inp[1].value;
     alert("here");

     const xhr = new XMLHttpRequest();
     xhr.open('POST', '/loginUser');
     xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
     xhr.onload = function() {
     if (xhr.status === 200) {
          // login successful
          window.location.href = "/dashboard";
     } else {
          alert("Username or password is wrong. Please try again.");
     }
     };
     xhr.send(`username=${username}&password=${password}`);
});

getAdmin.addEventListener("click", function() {
     let inp = document.getElementsByTagName("input");
     const username = inp[0].value;
     const password = inp[1].value;
     alert("here");

     const xhr = new XMLHttpRequest();
     xhr.open('POST', '/loginAdmin');
     xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
     xhr.onload = function() {
     if (xhr.status === 200) {
          // login successful
          window.location.href = "/admin";
     } else {
          alert("Username or password is wrong. Please try again.");
     }
     };
     xhr.send(`username=${username}&password=${password}`);
});

signIn.addEventListener("click", function (){

     const xhr = new XMLHttpRequest();
     xhr.open('POST', '/getData');
     xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
     xhr.onload = function() {
     if (xhr.status === 200) {
          alert("Successful.");
     } else {
          alert("Database connection is not successful!!");
     }
     };
     xhr.send("");

});

