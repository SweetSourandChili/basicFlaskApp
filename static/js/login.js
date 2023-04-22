
let userTable = document.getElementById("LoginTable");
let getUser = document.getElementById("readUser");
let getAdmin = document.getElementById("readAdmin");


getUser.addEventListener("click", function() {
     const username = userTable.querySelector('input[name="username"]').value;
     const password = userTable.querySelector('input[name="password"]').value;

     const xhr = new XMLHttpRequest();
     xhr.open('POST', '/login');
     xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
     xhr.onload = function() {
          const resp = JSON.parse(xhr.responseText);
          if (xhr.status === 200) {
               window.location.href = "/";
          } else {
               alert(resp.message);
          }
     };
     xhr.send(`username=${username}&password=${password}admin=False`);
});

getAdmin.addEventListener("click", function() {
     const username = userTable.querySelector('input[name="username"]').value;
     const password = userTable.querySelector('input[name="password"]').value;

     const xhr = new XMLHttpRequest();
     xhr.open('POST', '/login');
     xhr.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded');
     xhr.onload = function() {
          const resp = JSON.parse(xhr.responseText);
          if (xhr.status === 200) {
               window.location.href = "/admin";
          } else {
               alert(resp.message);
          }
     };
     xhr.send(`username=${username}&password=${password}&admin=True`);
});



