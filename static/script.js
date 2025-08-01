// OYSLOE Landing Page JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Track page view automatically when page loads
    trackPageView();
    
    // Mobile menu toggle
    const hamburger = document.querySelector('.hamburger');
    const mobileMenu = document.querySelector('.mobile-menu');
    
    if (hamburger && mobileMenu) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            mobileMenu.classList.toggle('active');
        });
    }

    // Mobile navbar scroll behavior
    let lastScrollTop = 0;
    const navbar = document.querySelector('.navbar');
    
    if (navbar) {
        window.addEventListener('scroll', function() {
            const scrollTop = window.pageYOffset || document.documentElement.scrollTop;
            
            // Only apply on mobile devices
            if (window.innerWidth <= 768) {
                if (scrollTop > lastScrollTop && scrollTop > 100) {
                    // Scrolling down - hide navbar
                    navbar.classList.add('navbar-hidden');
                } else {
                    // Scrolling up - show navbar
                    navbar.classList.remove('navbar-hidden');
                }
            } else {
                // On desktop, always show navbar
                navbar.classList.remove('navbar-hidden');
            }
            
            lastScrollTop = scrollTop;
        });
        
        // Handle window resize (orientation change, etc.)
        window.addEventListener('resize', function() {
            if (window.innerWidth > 768) {
                // On desktop, always show navbar
                navbar.classList.remove('navbar-hidden');
            }
        });
    }

    // Smooth scrolling for anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });

    // Form submission handling - prevent double submission
    const submitButton = document.getElementById('submit-seller-btn');
    if (submitButton) {
        console.log('🔧 Setting up form submission handler...');
        
        // Remove all existing event listeners by cloning and replacing the button
        const newSubmitButton = submitButton.cloneNode(true);
        submitButton.parentNode.replaceChild(newSubmitButton, submitButton);
        
        // Add new event listener to the fresh button
        newSubmitButton.addEventListener('click', handleFormSubmission);
        console.log('✅ Form submission handler attached successfully');
    } else {
        console.log('❌ Submit button not found');
    }

    // Pricing toggle functionality
    const billingToggle = document.getElementById('billingToggle');
    if (billingToggle) {
        billingToggle.addEventListener('change', updatePricing);
    }

    // Initialize pricing display
    updatePricing();
});

// Track page view
async function trackPageView() {
    try {
        const response = await fetch('/api/track-pageview/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            console.log('Page view tracked:', data);
        }
    } catch (error) {
        console.error('Error tracking page view:', error);
    }
}

// Flag to prevent double submission
let isSubmitting = false;

// Handle seller form submission
async function handleFormSubmission(e) {
    console.log('=== FORM SUBMISSION STARTED ===');
    console.log('Timestamp:', new Date().toISOString());
    console.log('Event:', e);
    console.log('Current isSubmitting flag:', isSubmitting);
    
    e.preventDefault();
    
    // Prevent double submission
    if (isSubmitting) {
        console.log('❌ Form submission already in progress...');
        return;
    }
    
    console.log('✅ Setting submission flag to true');
    const submitButton = document.getElementById('submit-seller-btn');
    const originalText = submitButton.textContent;
    
    // Set submission flag
    isSubmitting = true;
    
    // Show loading state and disable button immediately
    submitButton.textContent = 'Submitting...';
    submitButton.disabled = true;
    submitButton.style.pointerEvents = 'none';
    
    // Add a small delay to prevent rapid clicking
    await new Promise(resolve => setTimeout(resolve, 100));
    
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

        console.log('Submitting form data:', formData);

        // Submit to Django API
        const response = await fetch('/api/submit-seller/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCookie('csrftoken')
            },
            body: JSON.stringify(formData)
        });

        console.log('Response status:', response.status);

        if (!response.ok) {
            const errorData = await response.json();
            throw new Error(errorData.error || errorData.message || 'Failed to submit application. Please try again.');
        }

        const result = await response.json();
        console.log('Submission successful:', result);
        
        // Show success message
        showNotification('Application submitted successfully! We will contact you within 24 hours.', 'success');
        
        // Clear form
        clearForm();
        
    } catch (error) {
        console.error('Form submission error:', error);
        showNotification(error.message || 'An error occurred. Please try again.', 'error');
    } finally {
        // Reset submission flag and button state
        console.log('🔄 Resetting submission flag and button state');
        isSubmitting = false;
        submitButton.textContent = originalText;
        submitButton.disabled = false;
        submitButton.style.pointerEvents = 'auto';
        console.log('✅ Form submission completed');
    }
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