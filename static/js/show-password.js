document.getElementById("showPassword").addEventListener("change", function() {
    let password = document.getElementById("password");
    let confirmPassword = document.getElementById("confirm_password");
    let type = this.checked ? "text" : "password";
    password.type = type;
    confirmPassword.type = type;
});