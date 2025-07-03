// Create floating particles
function createParticles() {
    const particlesContainer = document.getElementById('particles');
    const particleCount = 50;

    for (let i = 0; i < particleCount; i++) {
        const particle = document.createElement('div');
        particle.className = 'particle';
        particle.style.left = Math.random() * 100 + '%';
        particle.style.animationDelay = Math.random() * 6 + 's';
        particle.style.animationDuration = (Math.random() * 3 + 3) + 's';

        // Random colors
        const colors = ['rgba(0, 212, 255, 0.6)', 'rgba(255, 0, 255, 0.6)', 'rgba(255, 255, 255, 0.3)'];
        particle.style.background = colors[Math.floor(Math.random() * colors.length)];

        particlesContainer.appendChild(particle);
    }
}

// Show notification
function showNotification() {
    const notification = document.getElementById('notification');
    setTimeout(() => {
        notification.classList.add('show');
    }, 3000);

    setTimeout(() => {
        notification.classList.remove('show');
    }, 8000);
}

// Add click effect to features
function addClickEffects() {
    const features = document.querySelectorAll('.feature');
    features.forEach(feature => {
        feature.addEventListener('click', function () {
            this.style.transform = 'scale(0.95)';
            setTimeout(() => {
                this.style.transform = 'translateY(-5px)';
            }, 150);
        });
    });
}

// Smooth scroll effect for mouse movement
function addMouseEffect() {
    document.addEventListener('mousemove', (e) => {
        const particles = document.querySelectorAll('.particle');
        const x = e.clientX / window.innerWidth;
        const y = e.clientY / window.innerHeight;

        particles.forEach((particle, index) => {
            const speed = (index % 5 + 1) * 0.5;
            const xOffset = (x - 0.5) * speed;
            const yOffset = (y - 0.5) * speed;

            particle.style.transform += ` translate(${xOffset}px, ${yOffset}px)`;
        });
    });
}

// Initialize everything when page loads
document.addEventListener('DOMContentLoaded', function () {
    createParticles();
    showNotification();
    addClickEffects();
    updateProgress();
    addMouseEffect();

    // Add some console messages for developers
    console.log('🚀 POBucket - Under Development');
    console.log('💻 Built with HTML, CSS, and JavaScript');
    console.log('🎨 Dark theme activated');
});

// Add keyboard shortcuts
document.addEventListener('keydown', function (e) {
    if (e.key === 'Enter' || e.key === ' ') {
        const notification = document.getElementById('notification');
        notification.classList.toggle('show');
    }
});
