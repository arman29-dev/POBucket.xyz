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

document.addEventListener('DOMContentLoaded', function () {
    const codeInputs = document.querySelectorAll('.code-input');
    const verifyButton = document.getElementById('verifyButton');
    const resendButton = document.getElementById('resendButton');
    const timer = document.getElementById('timer');
    const errorMessage = document.getElementById('errorMessage');
    const successMessage = document.getElementById('successMessage');

    let resendTimer = 60;
    let timerInterval;

    // Start resend timer
    startResendTimer();

    // Handle input navigation and validation
    codeInputs.forEach((input, index) => {
        input.addEventListener('input', function (e) {
            const value = e.target.value;

            // Only allow numbers
            if (!/^\d$/.test(value)) {
                e.target.value = '';
                return;
            }

            // Move to next input
            if (value && index < codeInputs.length - 1) {
                codeInputs[index + 1].focus();
            }

            checkCodeComplete();
        });

        input.addEventListener('keydown', function (e) {
            // Handle backspace
            if (e.key === 'Backspace' && !e.target.value && index > 0) {
                codeInputs[index - 1].focus();
            }

            // Handle paste
            if (e.key === 'v' && (e.ctrlKey || e.metaKey)) {
                e.preventDefault();
                navigator.clipboard.readText().then(text => {
                    const digits = text.replace(/\D/g, '').slice(0, 6);
                    digits.split('').forEach((digit, i) => {
                        if (codeInputs[i]) {
                            codeInputs[i].value = digit;
                        }
                    });
                    checkCodeComplete();
                });
            }
        });
    });

    // Check if all inputs are filled
    function checkCodeComplete() {
        const code = Array.from(codeInputs).map(input => input.value).join('');
        verifyButton.disabled = code.length !== 6;

        // Hide error message when user starts typing
        if (errorMessage.style.display === 'block') {
            errorMessage.style.display = 'none';
        }
    }

    // Handle verification
    verifyButton.addEventListener('click', async function () {
        const code = Array.from(codeInputs).map(input => input.value).join('');

        // Show loading state
        verifyButton.disabled = true;
        verifyButton.textContent = 'Verifying...';

        try {
            const { apiUrl, id } = API_DATA;
            // Post verification code to backend
            const response = await fetch(apiUrl, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    "X-CSRFToken": getCookie('csrftoken')
                },
                body: JSON.stringify({
                    code: code,
                    id: id
                })
            });

            const result = await response.json();

            if (response.ok && result.success) {
                // Verification successful
                successMessage.style.display = 'block';
                errorMessage.style.display = 'none';

                setTimeout(() => {
                    // Redirect to dashboard or next page
                    window.location.href = result.redirectUrl || '/buyer/login/';
                }, 2000);
            } else {
                // Verification failed
                throw new Error(result.message || 'Invalid verification code');
            }

        } catch (error) {
            // Handle errors
            errorMessage.textContent = error.message || 'Verification failed. Please try again.';
            errorMessage.style.display = 'block';
            successMessage.style.display = 'none';

            // Clear inputs and focus first one
            codeInputs.forEach(input => input.value = '');
            codeInputs[0].focus();
            checkCodeComplete();

            console.error('Verification error:', error);
        } finally {
            // Reset button state
            verifyButton.disabled = false;
            verifyButton.textContent = 'Verify Email';
        }
    });

    // Handle resend
    resendButton.addEventListener('click', async function () {
        const { apiUrl, id } = API_DATA;
        if (!resendButton.disabled) {
            try {
                // Show loading state
                resendButton.disabled = true;
                resendButton.textContent = 'Sending...';

                // Call backend to resend verification code
                const response = await fetch(apiUrl, {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json',
                        "X-CSRFToken": getCookie('csrftoken')
                    },
                    body: JSON.stringify({
                        id: id
                    })
                });

                const result = await response.json();

                if (response.ok && result.success) {
                    // Reset timer and UI
                    resendTimer = 60;
                    startResendTimer();

                    // Clear inputs
                    codeInputs.forEach(input => input.value = '');
                    codeInputs[0].focus();
                    checkCodeComplete();

                    // Hide messages
                    errorMessage.style.display = 'none';
                    successMessage.style.display = 'none';

                    console.log('Verification code resent successfully');
                } else {
                    throw new Error(result.message || 'Failed to resend verification code');
                }

            } catch (error) {
                errorMessage.textContent = error.message || 'Failed to resend code. Please try again.';
                errorMessage.style.display = 'block';
                console.error('Resend error:', error);
            } finally {
                // Reset button state if there was an error
                if (resendButton.disabled && resendTimer <= 0) {
                    resendButton.disabled = false;
                    resendButton.textContent = 'Resend code';
                }
            }
        }
    });

    function startResendTimer() {
        resendButton.disabled = true;

        timerInterval = setInterval(() => {
            timer.textContent = `(${resendTimer}s)`;
            resendTimer--;

            if (resendTimer < 0) {
                clearInterval(timerInterval);
                timer.textContent = '';
                resendButton.disabled = false;
                resendTimer = 60;
            }
        }, 1000);
    }

    // Focus first input on load
    codeInputs[0].focus();
});
