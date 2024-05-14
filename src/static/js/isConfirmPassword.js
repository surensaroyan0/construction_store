function isConfirmPassword() {
    let password = document.getElementById("password").value;
    let confirmPassword = document.getElementById("confirm_password").value;
    let passwordError = document.getElementById("password_error");

    if (password != confirmPassword) {
        passwordError.style.display = "block";
        return false;
    } else {
        return true;
    }
}