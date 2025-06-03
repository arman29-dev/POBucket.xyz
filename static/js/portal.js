document.addEventListener("DOMContentLoaded", () => {
    const form = document.getElementById('userProfileForm');
    const submitBtn = document.getElementById('submitBtn');

    // Store original values per input
    const inputs = form.querySelectorAll('.user-input');
    const originalValues = new Map();

    // Init values on modal open
    const modal = document.getElementById('user-profile-modal');
    modal.addEventListener('shown.bs.modal', () => {
      inputs.forEach(input => {
        input.setAttribute('readonly', true); // always reset to readonly
        input.setAttribute('disabled', true); // always reset to disabled
        originalValues.set(input, input.value); // store original values
      });
      submitBtn.disabled = true;
    });

    // Edit button click — enable input
    form.querySelectorAll('.data-edit-btn').forEach(button => {
      button.addEventListener('click', () => {
        const row = button.closest('.row');
        const input = row.querySelector('.user-input');
        input.removeAttribute('readonly');
        input.removeAttribute('disabled');
        input.focus();
      });
    });

    // Cancel button click — restore original value and readonly
    form.querySelectorAll('.cnl-data-edit-btn').forEach(button => {
      button.addEventListener('click', () => {
        const row = button.closest('.row');
        const input = row.querySelector('.user-input');
        const original = originalValues.get(input);
        input.value = original || '';
        input.setAttribute('readonly', true);
        input.setAttribute('disabled', true);
        checkIfChanged(); // update submit button state
      });
    });

    // On any input change — check for submit eligibility
    form.addEventListener('input', () => checkIfChanged());

    function checkIfChanged() {
      const changed = Array.from(inputs).some(input => input.value !== originalValues.get(input));
      submitBtn.disabled = !changed;
    }

    // Function to truncate text to a specified number of words
    function truncateText(text, limit) {
        const words = text.split(" ");
        if (words.length > limit) {
            return words.slice(0, limit).join(" ") + "...";
        }
        return text;
    }

    // Apply truncation to all item card description paragraphs
    const itemCardDesc = document.querySelectorAll(".item-desc");
    itemCardDesc.forEach((description) => {
        const fullText = description.textContent;
        const truncatedText = truncateText(fullText, 20);
        description.textContent = truncatedText;
    });

    // Apply truncation to all modal item description paragraphs
    const modalItemDesc =
        document.querySelectorAll(".modal-item-desc");
    modalItemDesc.forEach((description) => {
        const fullText = description.textContent;
        const truncatedText = truncateText(fullText, 20);
        description.textContent = truncatedText;

        // Add a "Read More" link if the text was truncated
        if (fullText !== truncatedText) {
            const readMoreLink = document.createElement("a");
            readMoreLink.href = "#";
            readMoreLink.textContent = " Read More";
            readMoreLink.classList.add("read-more-link");
            description.appendChild(readMoreLink);

            readMoreLink.addEventListener("click", function (e) {
                e.preventDefault();
                if (this.textContent === " Read More") {
                    description.textContent = fullText;
                    this.textContent = " Read Less";
                    description.appendChild(this);
                } else {
                    description.textContent = truncatedText;
                    this.textContent = " Read More";
                    description.appendChild(this);
                }
            });
        }
    });

    // Select all bid forms
    document.querySelectorAll(".input-group").forEach((form) => {
        form.addEventListener("submit", function (event) {
            // Get the highest bid value from the modal
            let highestBid = parseFloat(
                form
                    .closest(".modal-body")
                    .querySelector(".highest-bid").dataset
                    .highestBid,
            );

            // Get the user-entered bid amount
            let userBid = parseFloat(
                form.querySelector("#bit-input-field").value,
            );

            if (isNaN(userBid) || userBid <= highestBid) {
                alert(
                    "Your bid must be higher than the current highest bid (₹" +
                        highestBid +
                        ")",
                );
                event.preventDefault(); // Prevent form submission
            }
        });
    });
});

function validateUpdatedProfileData() {
  var username = document.getElementById("updatedUsername").value.trim();
  var email = document.getElementById("updatedEmail").value.trim();
  var phoneNo = document.getElementById("updatedPhoneNo").value.trim();

  var usernameRegX = /^@[a-zA-Z0-9_-]{3,15}$/;
  var emailRegX = /^[^@ \t\r\n]+@[^@ \t\r\n]+\.[^@ \t\r\n]+$/;
  var phoneNoRegX = /^[\+][(]?[0-9]{1,4}[)]?[-\s\.]?[0-9]{3,4}[-\s\.]?[0-9]{4}$/;

  let errorMsg = "";

  if (!usernameRegX.test(username)) {
    errorMsg = "Invalid Username. Use '@' and 8-15 lower & upper case alphanumeric characters or underscores.";
  } else if (!emailRegX.test(email)) {
    errorMsg = "Invalid Email format.";
  } else if (!phoneNoRegX.test(phoneNo)) {
    errorMsg = "Invalid Phone Number. Make sure you've typed the correct country code and 10 digits of your phone no.";
  }

  if (errorMsg !== "") {
    document.getElementById("error-msg").innerText = errorMsg;

    const toastElement = document.getElementById('profile-toast');
    toastElement.classList.add('toast-slide-down');

    const toast = new bootstrap.Toast(toastElement);
    toast.show();

    setTimeout(() => {
        toastElement.classList.remove('toast-slide-down');
    }, 400); return false;
  }
  return true;

}
