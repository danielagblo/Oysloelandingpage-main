// OYSLOE Landing Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Mobile menu toggle
    const hamburger = document.querySelector('.hamburger');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (hamburger && mobileMenu) {
    hamburger.addEventListener('click', function() {
        hamburger.classList.toggle('active');
        mobileMenu.classList.toggle('active');
        });
    }

    // Smooth scrolling for anchor links
    const anchorLinks = document.querySelectorAll('a[href^="#"]');
    
    anchorLinks.forEach(link => {
        link.addEventListener('click', function(e) {
            e.preventDefault();
            
            const targetId = this.getAttribute('href');
            const targetSection = document.querySelector(targetId);
            
            console.log('Anchor link clicked:', targetId); // Debug log
            
            if (targetSection) {
                // Smooth scroll to the target section
                targetSection.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
                
                // Update URL without page jump
                history.pushState(null, null, targetId);
                
                console.log('Scrolled to section:', targetId); // Debug log
            } else {
                console.log('Target section not found:', targetId); // Debug log
            }
        });
    });

    // Specifically handle the Start Selling button
    const startSellingBtn = document.querySelector('a[href="#seller-form"]');
    if (startSellingBtn) {
        console.log('Start Selling button found'); // Debug log
        startSellingBtn.addEventListener('click', function(e) {
            console.log('Start Selling button clicked!'); // Debug log
        });
    } else {
        console.log('Start Selling button not found'); // Debug log
    }

    // Form submission handling
    const submitButton = document.getElementById('submit-seller-btn');
    console.log('Submit button found:', submitButton); // Debug log
    if (submitButton) {
        submitButton.addEventListener('click', handleFormSubmission);
        console.log('Event listener attached to submit button'); // Debug log
    } else {
        console.error('Submit button not found!'); // Debug log
    }

    // Pricing toggle functionality
    const billingToggle = document.getElementById('billingToggle');
    if (billingToggle) {
        billingToggle.addEventListener('change', updatePricing);
    }

    // Initialize pricing display
    updatePricing();
});

// Handle seller form submission
async function handleFormSubmission(e) {
    e.preventDefault();
    
    const submitButton = document.getElementById('submit-seller-btn');
    const originalText = submitButton.textContent;
    
    // Show loading state
    submitButton.textContent = 'Submitting...';
    submitButton.disabled = true;
    
    try {
        // Get form data
        const formData = {
            owner_name: document.getElementById('owner-name').value.trim(),
            phone_number: document.getElementById('phone-number').value.trim(),
            email_address: document.getElementById('email-address').value.trim(),
            location: document.getElementById('location').value.trim(),
            business_name: document.getElementById('business-name').value.trim(),
            business_type: document.getElementById('business-type').value,
            experience_level: document.getElementById('experience-level').value,
            inventory_size: document.getElementById('inventory-size').value,
            business_description: document.getElementById('business-description').value.trim(),
            motivation: document.getElementById('motivation').value.trim()
        };

        // Validate required fields
        const requiredFields = [
            'owner_name', 'phone_number', 'email_address', 'location',
            'business_name', 'business_type', 'experience_level', 
            'inventory_size', 'business_description', 'motivation'
        ];

        for (const field of requiredFields) {
            if (!formData[field]) {
                throw new Error(`Please fill in all required fields. Missing: ${field.replace('_', ' ')}`);
            }
        }

        // Validate email format
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        if (!emailRegex.test(formData.email_address)) {
            throw new Error('Please enter a valid email address');
        }

        // Validate phone number (basic validation for Ghana numbers)
        const phoneRegex = /^(\+233|0)[0-9]{9}$/;
        if (!phoneRegex.test(formData.phone_number)) {
            throw new Error('Please enter a valid Ghana phone number (e.g., 0552891234 or +233552891234)');
        }

        // Submit to Django API
        const response = await fetch('/api/sellers/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(formData)
        });

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.message || 'Failed to submit application. Please try again.');
        }

        const result = await response.json();
        
        // Show success message
        showNotification('Application submitted successfully! We will contact you within 24 hours.', 'success');
        
        // Clear form
        clearForm();
        
    } catch (error) {
        console.error('Form submission error:', error);
        showNotification(error.message || 'An error occurred. Please try again.', 'error');
    } finally {
        // Reset button state
        submitButton.textContent = originalText;
        submitButton.disabled = false;
    }
}

// Clear form after successful submission
function clearForm() {
    const formFields = [
        'owner-name', 'phone-number', 'email-address', 'location',
        'business-name', 'business-type', 'experience-level', 
        'inventory-size', 'business-description', 'motivation'
    ];
    
    formFields.forEach(fieldId => {
        const element = document.getElementById(fieldId);
        if (element) {
            element.value = '';
        }
    });
}

// Show notification message
function showNotification(message, type = 'info') {
    // Remove existing notifications
    const existingNotification = document.querySelector('.notification');
    if (existingNotification) {
        existingNotification.remove();
    }

    // Create notification element
    const notification = document.createElement('div');
    notification.className = `notification notification-${type}`;
    notification.innerHTML = `
        <div class="notification-content">
            <span class="notification-message">${message}</span>
            <button class="notification-close">&times;</button>
        </div>
    `;

    // Add styles
    notification.style.cssText = `
        position: fixed;
        top: 20px;
        right: 20px;
        z-index: 10000;
        padding: 15px 20px;
        border-radius: 8px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.15);
        max-width: 400px;
        animation: slideIn 0.3s ease-out;
        font-family: 'Poppins', sans-serif;
    `;

    // Set background color based on type
    if (type === 'success') {
        notification.style.backgroundColor = '#10b981';
        notification.style.color = 'white';
    } else if (type === 'error') {
        notification.style.backgroundColor = '#ef4444';
        notification.style.color = 'white';
    } else {
        notification.style.backgroundColor = '#3b82f6';
        notification.style.color = 'white';
    }

    // Add to page
    document.body.appendChild(notification);

    // Add close functionality
    const closeButton = notification.querySelector('.notification-close');
    closeButton.addEventListener('click', () => {
        notification.remove();
    });

    // Auto remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Get CSRF token from cookies
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Pricing toggle functionality
function updatePricing() {
    const billingToggle = document.getElementById('billingToggle');
    const priceElements = document.querySelectorAll('.price');
    const periodElements = document.querySelectorAll('.period');
    
    if (!billingToggle) return;

    const isYearly = billingToggle.checked;
    
    priceElements.forEach(priceElement => {
        const monthlyPrice = priceElement.getAttribute('data-monthly');
        const yearlyPrice = priceElement.getAttribute('data-yearly');
        
        if (isYearly) {
            priceElement.textContent = yearlyPrice;
        } else {
            priceElement.textContent = monthlyPrice;
        }
    });

    periodElements.forEach(periodElement => {
        if (isYearly) {
            periodElement.textContent = '/month (billed yearly)';
        } else {
            periodElement.textContent = '/month';
        }
    });

    // Update billing toggle labels
    const labels = document.querySelectorAll('.billing-toggle-label');
    labels.forEach(label => {
        if (isYearly && label.getAttribute('data-billing-period') === 'yearly') {
            label.classList.add('active');
        } else if (!isYearly && label.getAttribute('data-billing-period') === 'monthly') {
            label.classList.add('active');
        } else {
            label.classList.remove('active');
        }
    });
}

// Add CSS animations
const style = document.createElement('style');
style.textContent = `
    @keyframes slideIn {
        from {
            transform: translateX(100%);
            opacity: 0;
        }
        to {
            transform: translateX(0);
            opacity: 1;
        }
    }

    .notification-content {
        display: flex;
        align-items: center;
        justify-content: space-between;
        gap: 10px;
    }

    .notification-close {
        background: none;
        border: none;
        color: inherit;
        font-size: 18px;
        cursor: pointer;
        padding: 0;
        width: 20px;
        height: 20px;
        display: flex;
        align-items: center;
        justify-content: center;
        opacity: 0.7;
    }

    .notification-close:hover {
        opacity: 1;
    }

    .billing-toggle-label.active {
        color: #2563eb;
        font-weight: 600;
    }
`;
document.head.appendChild(style);

// Countdown Timer Functionality
function updateCountdown() {
    // Set the launch date (you can modify this to your desired launch date)
    const launchDate = new Date('2024-12-31T00:00:00').getTime();
    const now = new Date().getTime();
    const distance = launchDate - now;

    if (distance > 0) {
        const days = Math.floor(distance / (1000 * 60 * 60 * 24));
        const hours = Math.floor((distance % (1000 * 60 * 60 * 24)) / (1000 * 60 * 60));
        const minutes = Math.floor((distance % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((distance % (1000 * 60)) / 1000);

        // Update the timer elements
        const daysElement = document.getElementById('days');
        const hoursElement = document.getElementById('hours');
        const minutesElement = document.getElementById('minutes');
        const secondsElement = document.getElementById('seconds');

        if (daysElement) daysElement.textContent = days.toString().padStart(2, '0');
        if (hoursElement) hoursElement.textContent = hours.toString().padStart(2, '0');
        if (minutesElement) minutesElement.textContent = minutes.toString().padStart(2, '0');
        if (secondsElement) secondsElement.textContent = seconds.toString().padStart(2, '0');
    } else {
        // Launch date has passed
        const countdownTimer = document.querySelector('.countdown-timer');
        if (countdownTimer) {
            countdownTimer.innerHTML = '<div class="launch-message"><h2>🎉 We\'re Live! 🎉</h2><p>OYSLOE Marketplace is now open for business!</p></div>';
        }
    }
}

// Initialize countdown timer when page loads
document.addEventListener('DOMContentLoaded', function() {
    // Start the countdown timer
    updateCountdown();
    
    // Update countdown every second
    setInterval(updateCountdown, 1000);
    
    // Initialize other existing functionality
    const billingToggle = document.getElementById('billingToggle');
    if (billingToggle) {
        billingToggle.addEventListener('change', updatePricing);
    }
}); 