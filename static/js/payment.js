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

	const amnt = "{{ total }}";

	// Call Django backend
	const response = await fetch(`/buyer/payment/${buyer}/${pid}`, {
		method: "POST",
		headers: {
			"Content-Type": "application/json",
			"X-CSRFToken": "{{ csrf_token }}"
		},
		body: JSON.stringify({
			amount: amnt,
			currency: "INR",
			order_id: orderId,
			method: "card",
			card: data
		})
	});

	const result = await response.json();
	console.log(result);

	if (result.status === "captured") {
		alert("Payment Successful!");
		window.location.href = `/buyer/payment/${buyer}/${pid}/verify/${orderId}`;
	} else {
		alert("Payment Failed: " + result.error);
	}
}