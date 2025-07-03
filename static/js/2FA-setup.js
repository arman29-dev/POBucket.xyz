document.getElementById('verificationCode').addEventListener('input', function (e) {
    let value = e.target.value.replace(/\D/g, ''); // Remove non-digits
    if (value.length > 6) {
        value = value.slice(0, 6);
    }
    e.target.value = value;

    if (value.length === 6) {
        setTimeout(() => {
            verifyCode();
        }, 500);
    }
});

function copyToClipboard() {
    const manualCode = document.getElementById('manualCode').textContent.trim().replace(/\s+/g, '');
    const copyButton = document.getElementById('copyButton');

    navigator.clipboard.writeText(manualCode).then(() => {
        copyButton.textContent = '✅ Copied!';
        copyButton.classList.add('copied');

        document.getElementById('manualCode').classList.add('pulse');

        setTimeout(() => {
            copyButton.textContent = '📋 Copy Code';
            copyButton.classList.remove('copied');
            document.getElementById('manualCode').classList.remove('pulse');
        }, 2000);
    }).catch(() => {
        showStatus('Failed to copy code', 'error');
    });
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

async function verifyCode() {
    const code = document.getElementById('verificationCode').value;
    const verifyButton = document.getElementById('verifyButton');

    if (code.length !== 6) {
        showStatus('Please enter a 6-digit code', 'error');
        return;
    }

    verifyButton.disabled = true;
    verifyButton.textContent = 'Verifying...';

    try {
        const { apiUrl, seller_email, success_url } = API_DATA;
        const response = await fetch(apiUrl, {
            method: 'POST',
            headers: {
                'X-CSRFToken': getCookie('csrftoken'),
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                verification_code: code,
                seller_email: seller_email,
            }),
        });

        const data = await response.json();
        if (response.ok && data.success) {
            showStatus('✅ 2FA successfully enabled!', 'success');
            verifyButton.textContent = '2FA Enabled';
            document.getElementById('verificationCode').disabled = true;

            setTimeout(() => {
                window.location.href = success_url;
            }, 2000);

        } else {
            const errorMessage = data.error || data.message || 'Invalid verification code. Please try again.';
            showStatus(`❌ ${errorMessage}`, 'error');

            verifyButton.disabled = false;
            verifyButton.textContent = 'Verify & Enable 2FA';
            document.getElementById('verificationCode').focus();
            document.getElementById('verificationCode').select();
        }

    } catch (error) {
        console.error('2FA Verification Error:', error);

        showStatus('❌ Connection error. Please try again.', 'error');

        verifyButton.disabled = false;
        verifyButton.textContent = 'Verify & Enable 2FA';
    }
}

function showStatus(message, type) {
    const statusElement = document.getElementById('statusMessage');
    statusElement.textContent = message;
    statusElement.className = `status-message ${type} show`;

    if (type === 'error') {
        setTimeout(() => {
            statusElement.classList.remove('show');
        }, 5000);
    }
}

// Handle Enter key in input
document.getElementById('verificationCode').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        verifyCode();
    }
});
