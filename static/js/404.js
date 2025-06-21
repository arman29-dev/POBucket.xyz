// Search functionality
function performSearch() {
    const searchTerm = document.getElementById('searchInput').value.trim();
    if (searchTerm) {
        showNotification(`Searching for "${searchTerm}"...`, 'info');
        setTimeout(() => {
            // In a real application, this would perform an actual search
            window.location.href = `/search?q=${encodeURIComponent(searchTerm)}`;
        }, 1000);
    } else {
        showNotification('Please enter a search term', 'warning');
    }
}

// Handle Enter key in search input
document.getElementById('searchInput').addEventListener('keypress', function (e) {
    if (e.key === 'Enter') {
        performSearch();
    }
});

// Navigation functions
function goHome() {
    showNotification('Redirecting to homepage...', 'info');
    setTimeout(() => {
        window.location.href = '/';
    }, 1000);
}

function goBack() {
    showNotification('Going back...', 'info');
    setTimeout(() => {
        window.history.back();
    }, 1000);
}

function goToPage(url) {
    showNotification('Redirecting...', 'info');
    setTimeout(() => {
        window.location.href = url;
    }, 1000);
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
        <h3 style="color: #ffffff; font-size: 1.5rem; margin-bottom: 20px; text-align: center;">Need Help Finding Something?</h3>
        <p style="color: #d0d0d0; margin-bottom: 20px;">Our support team can help you locate the page or content you're looking for.</p>
        <div style="margin-bottom: 20px;">
            <p style="color: #a0a0a0; margin-bottom: 5px;">Email Support:</p>
            <p style="color: #63d4ff; font-weight: 600;">support@pobucket.com</p>
        </div>
        <div style="margin-bottom: 20px;">
            <p style="color: #a0a0a0; margin-bottom: 5px;">Phone Support:</p>
            <p style="color: #63d4ff; font-weight: 600;">+91 12345 67890</p>
        </div>
        <div style="margin-bottom: 20px;">
            <p style="color: #a0a0a0; margin-bottom: 5px;">Live Chat:</p>
            <p style="color: #63d4ff; font-weight: 600;">Available 24/7 on our website</p>
        </div>
        <div style="margin-bottom: 20px;">
            <p style="color: #a0a0a0; margin-bottom: 5px;">Requested URL:</p>
            <p style="color: #ff6b6b; font-weight: 600; word-break: break-all;">${window.location.href}</p>
        </div>
        <button id="closeSupportModal" style="background: linear-gradient(135deg, #63d4ff, #4fc3f7); color: #1a1a1a; border: none; padding: 12px 25px; border-radius: 50px; font-weight: 600; cursor: pointer; display: block; margin: 0 auto; box-shadow: 0 5px 15px rgba(99, 212, 255, 0.3);">Close</button>
    `;

    supportModal.appendChild(modalContent);
    document.body.appendChild(supportModal);

    document.getElementById('closeSupportModal').addEventListener('click', function () {
        supportModal.style.animation = 'fadeOut 0.3s ease-out';
        setTimeout(() => {
            document.body.removeChild(supportModal);
        }, 300);
    });
}

// Show notification function
function showNotification(message, type) {
    const notification = document.createElement('div');
    const bgColor = type === 'info' ? '#63d4ff' : type === 'warning' ? '#ffa726' : '#4CAF50';
    const textColor = type === 'info' ? '#1a1a1a' : 'white';

    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${bgColor};
        color: ${textColor};
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
    // Add hover effect to search container
    const searchContainer = document.querySelector('.search-container');
    searchContainer.addEventListener('mouseenter', function () {
        this.style.transform = 'scale(1.02)';
        this.style.transition = 'transform 0.3s ease';
    });

    searchContainer.addEventListener('mouseleave', function () {
        this.style.transform = 'scale(1)';
    });

    // Add click effect to the illustration
    const illustration = document.querySelector('.not-found-illustration');
    illustration.addEventListener('click', function () {
        this.style.animation = 'none';
        setTimeout(() => {
            this.style.animation = 'bounceIn 0.6s ease-out, floating 3s ease-in-out infinite';
        }, 10);
    });

    // Focus on search input when page loads
    setTimeout(() => {
        document.getElementById('searchInput').focus();
    }, 1000);
});
