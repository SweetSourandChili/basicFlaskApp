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

var loggedInOperations = function (){

}