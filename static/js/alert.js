document.addEventListener("DOMContentLoaded", () => {
  const alerts = document.querySelectorAll(".custom-alert");
  alerts.forEach((alert) => {
      setTimeout(() => {
          alert.classList.add("fade-out");
          setTimeout(() => {
              alert.remove();
          }, 500);
      }, 5000);
  });

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
