document.addEventListener("DOMContentLoaded", () => {
    const paymentButton = document.getElementById("payment-button")
    const form = document.querySelector("form")

    form.addEventListener("submit", async function(e) {
        e.preventDefault()

        const cardNumber = document.querySelectorAll(".input-card-number")
        const cardHolder = document.getElementById("card-holder")
        const expDate = document.getElementById("exp")
        const ccv = document.getElementById("card-ccv")

        let isValid = true

        cardNumber.forEach((input) => {
            if (input.value.length < 4) isValid = false
        })

        if (!cardHolder.value || !expDate.value || !ccv.value) {
            isValid = false
        }

        if (!isValid) {
            paymentButton.classList.add("error")
            setTimeout(() => {
                paymentButton.classList.remove("error")
            }, 500)
            return
        }

    });

    const buyer = "{{ buyer }}";
    const pid = "{{ pid }}";

    document.getElementById("payment-button").addEventListener("click", async function (e) {
        e.preventDefault();

        paymentButton.classList.add("processing")
        paymentButton.querySelector(".btn-text").textContent = "Processing..."

        const orderId = result.order_id;
        console.log("✅ Order ID: ", orderId);

        processCardPayment(orderId);
    });

    async function processCardPayment(orderId) {
        const cardNumberInputs = document.querySelectorAll(".card-number-input");
        const CardNumber = Array.from(cardNumberInputs).map(input => input.value).join('');

        var expDate = document.getElementById("exp").value.split("/");
        var data = {
            card_number: CardNumber,
            exp_month: parseInt(expDate[0], 10),
            exp_year: parseInt(expDate[1], 10),
            cvv: document.getElementById("card-ccv").value,
            name: document.getElementById("card-holder").value
        };

        const famnt = "{{ total }}";
        const amnt = parseInt(famnt);

        const response = await fetch("", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": "{{ csrf_token }}"
            },
        });

        const rzp_data = await response.json();
        console.log(result);

      const options = {
        key: rzp_data.razorpay_key,
        amount: rzp_data.amount,
        currency: rzp_data.currency,
        name: "{{ product.name }}",
        description: "POBucket Purchase",
        order_id: rzp_data.order_id,
        handler: function (response) {
          fetch(`/payment/verify/{{ product.pid }}/`, {
            method: "POST",
            headers: {
              'Content-Type': 'application/json',
              'X-CSRFToken': '{{ csrf_token }}',
            },
            body: JSON.stringify(response)
          }).then(res => res.json()).then(result => {
            if (result.status === "success") {
              paymentButton.classList.remove("processing");
              paymentButton.querySelector(".btn-text").textContent = "Payment successful!";
              paymentButton.classList.add("success");
              window.location.href = `/buyer/payment/verify/${orderId}`;
            } else {
              paymentButton.classList.remove("processing");
              paymentButton.querySelector(".btn-text").textContent = "Payment failed!";
              paymentButton.classList.add("error");
              setTimeout(() => {
                paymentButton.classList.remove("error");
                paymentButton.querySelector(".btn-text").textContent = "Submit Payment";
              }, 2500);
              alert("Payment Failed: " + result.error);
            }
          });
        },
        prefill: {
          name: "{{ user.username }}",
          email: "{{ user.email }}",
          contact: "{{ user.phone_number }}"
        },
        theme: {
          color: "#000000",
          background: "#ffffff",
          button: {
            color: "#ffffff",
            background: "#000000"
          }
        }
      };

      const rzp = new Razorpay(options);
      rzp.open();
    }

    }

    // Add error animation
    const errorAnimation = `
      @keyframes shake {
        0%, 100% { transform: translateX(0); }
        10%, 30%, 50%, 70%, 90% { transform: translateX(-5px); }
        20%, 40%, 60%, 80% { transform: translateX(5px); }
      }
      .btn-payment.error {
        animation: shake 0.5s cubic-bezier(.36,.07,.19,.97) both;
        background: linear-gradient(135deg, #dc3545, #c82333);
      }
    `

    // Add the error animation styles
    const styleSheet = document.createElement("style")
    styleSheet.innerText = errorAnimation
    document.head.appendChild(styleSheet)
})

document.querySelectorAll('.input-card-number').forEach(function (input) {
    input.addEventListener('keyup', function () {
        if (this.value.length > 3) {
            let nextInput = this.nextElementSibling;
            if (nextInput) {
                nextInput.focus();
            }
        }

        let card_number = '';
        document.querySelectorAll('.input-card-number').forEach(function (input) {
            card_number += input.value + ' ';
            if (input.value.length == 4) {
                let nextInput = input.nextElementSibling;
                if (nextInput) {
                    nextInput.focus();
                }
            }
        });

        document.querySelector('.credit-card-box .number').innerHTML = card_number;
    });
});

document.getElementById('card-holder').addEventListener('keyup', function () {
    document.querySelector('.credit-card-box .card-holder div').innerHTML = this.value;
});

document.getElementById('card-holder').addEventListener('change', function () {
    document.querySelector('.credit-card-box .card-holder div').innerHTML = this.value;
});

document.getElementById('exp').addEventListener('keyup', formatExpirationDate);
document.getElementById('exp').addEventListener('change', formatExpirationDate);

function formatExpirationDate() {
    let expInput = document.getElementById('exp').value;
    let formattedExp = expInput;

    if (expInput.length === 2 && !expInput.includes('/')) {
        formattedExp = expInput + '/';
    } else if (expInput.length > 2 && !expInput.includes('/')) {
        formattedExp = expInput.slice(0, 2) + '/' + expInput.slice(2);
    }

    document.querySelector('.card-expiration-date div').innerHTML = formattedExp;
    document.getElementById('exp').value = formattedExp;
}

document.getElementById('card-ccv').addEventListener('focus', function () {
    document.querySelector('.credit-card-box').classList.add('hover');
});

document.getElementById('card-ccv').addEventListener('blur', function () {
    document.querySelector('.credit-card-box').classList.remove('hover');
});

document.getElementById('card-ccv').addEventListener('keyup', function () {
    document.querySelector('.ccv div').innerHTML = this.value;
});

document.getElementById('card-ccv').addEventListener('change', function () {
    document.querySelector('.ccv div').innerHTML = this.value;
});

setTimeout(function () {
    let ccvInput = document.getElementById('card-ccv');
    ccvInput.focus();
    setTimeout(function () {
        ccvInput.blur();
    }, 1000);
}, 500);

function getCreditCardType(accountNumber) {
    if (/^5[1-5]/.test(accountNumber)) {
        result = 'mastercard';
    } else if (/^4/.test(accountNumber)) {
        result = 'visa';
    } else if (/^(5018|5020|5038|6304|6759|676[1-3])/.test(accountNumber)) {
        result = 'maestro';
    } else {
        result = 'unknown'
    }
    return result;
}

document.getElementById('card-number').addEventListener('change', function () {
    console.log(getCreditCardType(this.value));
});
