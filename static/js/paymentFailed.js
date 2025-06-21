// Retry payment function
function retryPayment() {
    showNotification('Redirecting to payment page...', 'info');
    setTimeout(() => {
        window.location.href = '/payment';
    }, 1500);
}

// Contact support function
function contactSupport() {
    const supportModal = document.createElement('div');
    supportModal.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        width: 100%;
        height: 100%;
        background: rgba(0, 0, 0, 0.8);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 1000;
        animation: fadeIn 0.3s ease-out;
    `;

    const modalContent = document.createElement('div');
    modalContent.style.cssText = `
        background: rgba(40, 40, 40, 0.95);
        border-radius: 15px;
        padding: 30px;
        max-width: 500px;
        width: 90%;
        box-shadow: 0 15px 30px rgba(0, 0, 0, 0.3);
        border: 1px solid rgba(255, 255, 255, 0.1);
        position: relative;
        animation: slideUp 0.4s ease-out;
    `;

    modalContent.innerHTML = `
        <h3 style="color: #ffffff; font-size: 1.5rem; margin-bottom: 20px; text-align: center;">Contact Support</h3>
        <p style="color: #d0d0d0; margin-bottom: 20px;">Our support team is available 24/7 to help you resolve any payment issues.</p>
        <div style="margin-bottom: 20px;">
            <p style="color: #a0a0a0; margin-bottom: 5px;">Email:</p>
            <p style="color: #ff8c42; font-weight: 600;">support@pobucket.com</p>
        </div>
        <div style="margin-bottom: 20px;">
            <p style="color: #a0a0a0; margin-bottom: 5px;">Phone:</p>
            <p style="color: #ff8c42; font-weight: 600;">+91 12345 67890</p>
        </div>
        <div style="margin-bottom: 20px;">
            <p style="color: #a0a0a0; margin-bottom: 5px;">Live Chat:</p>
            <p style="color: #ff8c42; font-weight: 600;">Available on our website</p>
        </div>
        <div style="margin-bottom: 20px;">
            <p style="color: #a0a0a0; margin-bottom: 5px;">Reference:</p>
            <p style="color: #ff8c42; font-weight: 600;">Transaction ID: #TXN-2024-567890</p>
        </div>
        <button id="closeModal" style="background: linear-gradient(135deg, #ff5757, #ff8c42); color: white; border: none; padding: 12px 25px; border-radius: 50px; font-weight: 600; cursor: pointer; display: block; margin: 0 auto; box-shadow: 0 5px 15px rgba(255, 87, 87, 0.3);">Close</button>
    `;

    supportModal.appendChild(modalContent);
    document.body.appendChild(supportModal);

    document.getElementById('closeModal').addEventListener('click', function() {
        supportModal.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => {
            document.body.removeChild(supportModal);
        }, 300);
    });

    // Add animations
    const style = document.createElement('style');
    style.textContent = `
        @keyframes fadeIn {
            from { opacity: 0; }
            to { opacity: 1; }
        }
        @keyframes fadeOut {
            from { opacity: 1; }
            to { opacity: 0; }
        }
        @keyframes slideUp {
            from { transform: translateY(50px); opacity: 0; }
            to { transform: translateY(0); opacity: 1; }
        }
    `;
    document.head.appendChild(style);
}

// Show notification function
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'info' ? '#ff8c42' : '#ff5757'};
        color: white;
        padding: 15px 25px;
        border-radius: 10px;
        box-shadow: 0 5px 15px rgba(0,0,0,0.3);
        z-index: 1000;
        animation: slideInRight 0.3s ease-out;
        font-weight: 600;
    `;
    notification.textContent = message;
    document.body.appendChild(notification);

    setTimeout(() => {
        notification.style.animation = 'slideOutRight 0.3s ease-out';
        setTimeout(() => {
            document.body.removeChild(notification);
        }, 300);
    }, 3000);
}

// Add slide animations for notifications
const style = document.createElement('style');
style.textContent = `
    @keyframes slideInRight {
        from { transform: translateX(100%); opacity: 0; }
        to { transform: translateX(0); opacity: 1; }
    }
    @keyframes slideOutRight {
        from { transform: translateX(0); opacity: 1; }
        to { transform: translateX(100%); opacity: 0; }
    }
`;
document.head.appendChild(style);

// Add interactive effects
document.addEventListener('DOMContentLoaded', function() {
    // Add hover effect to error details
    const errorDetails = document.querySelector('.error-details');
    errorDetails.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.02)';
        this.style.transition = 'transform 0.3s ease';
    });

    errorDetails.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1)';
    });

    // Pulse animation for error mark
    const errorMark = document.querySelector('.error-mark');
    errorMark.addEventListener('click', function() {
        this.style.animation = 'none';
        setTimeout(() => {
            this.style.animation = 'pulseError 2s infinite';
        }, 10);
    });
});
