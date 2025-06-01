document.addEventListener("DOMContentLoaded", () => {
  // Auto-dismiss alerts after 5 seconds
  const alerts = document.querySelectorAll(".custom-alert");
  alerts.forEach((alert) => {
      setTimeout(() => {
          alert.classList.add("fade-out");
          setTimeout(() => {
              alert.remove();
          }, 500);
      }, 5000);
  });

  // Add click event for manual dismissal
  document.querySelectorAll(".alert-close").forEach((button) => {
      button.addEventListener("click", function () {
          const alert = this.closest(".custom-alert");
          alert.classList.add("fade-out");
          setTimeout(() => {
              alert.remove();
          }, 500);
      });
  });
})


// var emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
var usernameRegex = /^@[a-z0-9_-]{3,15}$/;
var passwordRegex =
    /^(?=.*?[A-Z])(?=.*?[a-z])(?=.*?[0-9])(?=.*?[#?!@$ %^&*-]).{8,}$/;
var errorMessage = "";

function validateRegistrationForm() {
    var username = document.getElementById("username").value;
    // var email = document.getElementById("email").value;
    var password = document.getElementById("password").value;
    var confirmPassword =
        document.getElementById("c-password").value;

    if (!usernameRegex.test(username)) {
        errorMessage =
            "Invalid username. Make sure to use '@' befor your username.";
    }
    // else if (!emailRegex.test(email)) {
    //     errorMessage =
    //         "Invalid email address. Make sure you've enter a valid email address.";
    // }
    else if (!passwordRegex.test(password)) {
        errorMessage =
            "Password should be >8 characters and contain ≥1 upper case, ≥1 lower case & ≥1 number.";
    } else if (password !== confirmPassword) {
        errorMessage =
            "Passwords do not match. Make sure you've entered the same password in both fields.";
    }

    if (errorMessage) {
        var errorDiv = document.getElementById(
            "sign-up-error-message",
        );

        if (!errorDiv) {
            errorDiv = document.createElement("div");
            errorDiv.id = "sign-up-error-message";
            errorDiv.style.color = "red";
            document
                .querySelector(".flip-card__back")
                .appendChild(errorDiv);
        }

        errorDiv.textContent = errorMessage;
        return false;
    }
    return true;
}

function validateLoginForm() {
    var email = document.getElementById("email").value;
    if (!emailRegex.test(email)) {
        errorMessage =
            "Invalid email address. Make sure you've enter a valid email address.";
    }

    if (errorMessage) {
        var errorDiv = document.getElementById(
            "login-error-message",
        );

        if (!errorDiv) {
            errorDiv = document.createElement("div");
            errorDiv.id = "login-error-message";
            errorDiv.style.color = "red";
            document
                .querySelector(".flip-card__front")
                .appendChild(errorDiv);
        }

        errorDiv.textContent = errorMessage;
        return false;
    }
    return true;
}
