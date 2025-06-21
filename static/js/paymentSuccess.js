document.addEventListener('DOMContentLoaded', function() {
    const now = new Date();
    const options = {
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    document.getElementById('transaction-date').textContent = now.toLocaleDateString('en-IN', options);
});


function downloadReceipt(order_id, amount, pay_method) {
    const receiptContent = `
        PAYMENT RECEIPT
        ===============

        Order ID: #ODR-${order_id}
        Date: ${new Date().toLocaleDateString('en-IN')}

        Product: Premium Wireless Headphones
        Amount: ₹${amount}
        Payment Method: ${pay_method}

        Thank you for your purchase!
        POBucket Team
    `;

    const blob = new Blob([receiptContent], { type: 'text/plain' });
    const url = window.URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = 'POBucket_Receipt_ODR-{{ order_id }}.txt';
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    window.URL.revokeObjectURL(url);

    showNotification('Receipt downloaded successfully!', 'success');
}


function trackOrder() {
    showNotification('Redirecting to order tracking...', 'info');
    setTimeout(() => {
        alert('This would redirect to the order tracking page with Order ID: #POB-2024-001234');
    }, 1000);
}


function continueShopping() {
    showNotification('Redirecting to shop...', 'info');
    setTimeout(() => {
        window.location.href = '/';
    }, 1000);
}


function showNotification(message, type) {
    const notification = document.createElement('div');
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        background: ${type === 'success' ? '#6bd4c7' : '#4CAF50'};
        color: #1a1a1a;
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


document.addEventListener('DOMContentLoaded', function() {
    // Add click effect to the success illustration
    const successIllustration = document.querySelector('.success-illustration');
    successIllustration.addEventListener('click', function() {
        this.style.animation = 'none';
        setTimeout(() => {
            this.style.animation = 'bounceIn 0.6s ease-out';
        }, 10);
    });


    const orderDetails = document.querySelector('.order-details');
    orderDetails.addEventListener('mouseenter', function() {
        this.style.transform = 'scale(1.02)';
        this.style.transition = 'transform 0.3s ease';
    });

    orderDetails.addEventListener('mouseleave', function() {
        this.style.transform = 'scale(1)';
    });
});


setTimeout(() => {
    if (confirm('Would you like to continue shopping? (Auto-redirect in 30 seconds)')) {
        continueShopping();
    }
}, 30000);
