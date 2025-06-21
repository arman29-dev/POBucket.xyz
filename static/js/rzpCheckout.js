function formatNumberWithCommas(num) {
    return num.toString().replace(/\B(?=(\d{3})+(?!\d))/g, ",");
}

document.addEventListener("DOMContentLoaded", function () {
    const price = document.getElementById("price");
    const priceRawValue = price.getAttribute("data-raw");

    const total = document.getElementById("total");
    const totalRawValue = total.getAttribute("data-raw");

    if (priceRawValue) {
        const number = parseFloat(priceRawValue);
        if (!isNaN(number)) {
            price.textContent = "₹" + formatNumberWithCommas(number);
        } else {
            console.warn("Invalid number in data-raw:", priceRawValue);
        }
    }

    if (totalRawValue) {
        const number = parseFloat(totalRawValue);
        if (!isNaN(number)) {
            total.textContent = "₹" + formatNumberWithCommas(number);
        } else {
            console.warn("Invalid number in data-raw:", totalRawValue);
        }
    }
});

function cancelPayment() {
    if (confirm('Are you sure you want to cancel this payment?')) {
        window.history.back();
    }
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            cookie = cookie.trim();
            if (cookie.startsWith(name + '=')) {
                cookieValue = decodeURIComponent(cookie.slice(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

document.getElementById("pay-btn").addEventListener("click", async function (e) {
    e.preventDefault();

    const button = document.querySelector('.payment-button');
    const buttonText = document.querySelector('.button-text');

    button.classList.add('loading');
    buttonText.textContent = 'Processing...';
    button.disabled = true;

    const response = await fetch("", {
        method: "POST",
        headers: {
            "X-CSRFToken": getCookie('csrftoken')
        }
    });

    const data = await response.json();
    const { fullname, userEmail, product_name } = RZP_CONTEXT;

    const options = {
        key: data.razorpay_key,
        amount: data.amount,
        currency: data.currency,
        name: product_name,
        description: "POBucket Purchase",
        order_id: data.order_id,
        handler: async function (response) {
            try {
                const paymentMethod = response.razorpay_payment_id ?
                    'Razorpay (' + (response.method || 'card') + ')' :
                    'Online Payment';

                // Send payment details to server for verification
                fetch('/buyer/payment/verify/', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        'X-CSRFToken': getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        razorpay_payment_id: response.razorpay_payment_id,
                        razorpay_order_id: response.razorpay_order_id,
                        razorpay_signature: response.razorpay_signature,
                        payment_method: paymentMethod,
                        product_name: product_name
                    })
                });
            } catch (error) {
                alert(error)
            }
        },
        prefill: {
            name: fullname,
            email: userEmail
        },
        theme: {
            color: "#3399cc"
        }
    };

    const rzp = new Razorpay(options);
    rzp.open();
});
