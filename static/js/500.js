// Refresh page function
function refreshPage() {
    showNotification('Refreshing page...', 'info');
    setTimeout(() => {
        location.reload();
    }, 1000);
}

// Go to homepage function
function goHome() {
    showNotification('Redirecting to homepage...', 'info');
    setTimeout(() => {
        window.location.href = '/';
    }, 1000);
}

// Check server status function
function checkStatus() {
    const statusModal = document.createElement('div');
    statusModal.style.cssText = `
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
        <h3 style="color: #ffffff; font-size: 1.5rem; margin-bottom: 20px; text-align: center;">Server Status</h3>
        <div style="margin-bottom: 20px;">
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                <div style="width: 12px; height: 12px; border-radius: 50%; background: #ff6b6b; animation: pulse 2s infinite;"></div>
                <span style="color: #ff6b6b; font-weight: 600;">Main Server: Down</span>
            </div>
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                <div style="width: 12px; height: 12px; border-radius: 50%; background: #ffa726;"></div>
                <span style="color: #ffa726; font-weight: 600;">Database: Maintenance</span>
            </div>
            <div style="display: flex; align-items: center; gap: 10px; margin-bottom: 15px;">
                <div style="width: 12px; height: 12px; border-radius: 50%; background: #4CAF50;"></div>
                <span style="color: #4CAF50; font-weight: 600;">CDN: Operational</span>
            </div>
        </div>
        <div style="background: rgba(255, 107, 107, 0.1); border-radius: 10px; padding: 15px; margin-bottom: 20px; border: 1px solid rgba(255, 107, 107, 0.2);">
            <p style="color: #d0d0d0; margin: 0; font-size: 0.9rem;">
                <strong style="color: #ff6b6b;">Current Issue:</strong> Server maintenance in progress.
                Expected resolution: 15-30 minutes.
            </p>
        </div>
        <button id="closeStatusModal" style="background: linear-gradient(135deg, #63d4ff, #4fc3f7); color: #1a1a1a; border: none; padding: 12px 25px; border-radius: 50px; font-weight: 600; cursor: pointer; display: block; margin: 0 auto; box-shadow: 0 5px 15px rgba(99, 212, 255, 0.3);">Close</button>
    `;

    statusModal.appendChild(modalContent);
    document.body.appendChild(statusModal);

    document.getElementById('closeStatusModal').addEventListener('click', function () {
        statusModal.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => {
            document.body.removeChild(statusModal);
        }, 300);
    });
}

// Show notification function
function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'info' ? '#63d4ff' : '#ff6b6b'};
        color: ${type === 'info' ? '#1a1a1a' : 'white'};
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

// Add slide animations for notifications and modals
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

// Add interactive effects
document.addEventListener('DOMContentLoaded', function () {
    // Add hover effect to error details
    const errorDetails = document.querySelector('.error-details');
    errorDetails.addEventListener('mouseenter', function () {
        this.style.transform = 'scale(1.02)';
        this.style.transition = 'transform 0.3s ease';
    });

    errorDetails.addEventListener('mouseleave', function () {
        this.style.transform = 'scale(1)';
    });

    // Add click effect to the server illustration
    const serverIllustration = document.querySelector('.server-illustration');
    serverIllustration.addEventListener('click', function () {
        this.style.animation = 'none';
        setTimeout(() => {
            this.style.animation = 'bounceIn 0.6s ease-out';
        }, 10);
    });

    // Auto-refresh attempt after 2 minutes
    setTimeout(() => {
        if (confirm('Would you like to try refreshing the page? The server might be back online.')) {
            refreshPage();
        }
    }, 120000); // 2 minutes
});
