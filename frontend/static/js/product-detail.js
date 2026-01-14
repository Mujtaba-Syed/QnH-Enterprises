// Product Detail Page JavaScript
// Handles image gallery, cart functionality, and other product-specific features

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    console.log('Product detail page loaded');
    console.log('Testing if functions are available...');
    console.log('loadRandomProducts function:', typeof loadRandomProducts);
    console.log('setupImageGallery function:', typeof setupImageGallery);
    
    setupImageGallery();
    loadRandomProducts();
    
    // Test API endpoint accessibility
    testAPIEndpoint();
    
    // Setup fallback thumbnails if main setup fails
    setTimeout(() => {
        if (document.querySelectorAll('#thumbnailContainer .thumbnail').length === 0) {
            console.log('Main setup failed, using fallback thumbnails');
            setupFallbackThumbnails();
        }
    }, 2000);
});

// Fallback thumbnail setup
function setupFallbackThumbnails() {
    const fallbackContainer = document.getElementById('fallbackThumbnails');
    const mainContainer = document.getElementById('thumbnailContainer');
    
    if (fallbackContainer && mainContainer) {
        // Move fallback thumbnails to main container
        const thumbnails = fallbackContainer.querySelectorAll('.thumbnail');
        thumbnails.forEach(thumb => {
            const newThumb = thumb.cloneNode(true);
            newThumb.addEventListener('click', function() {
                const imageSrc = this.getAttribute('data-image');
                const index = parseInt(this.getAttribute('data-index'));
                switchMainImage(imageSrc, index);
            });
            mainContainer.appendChild(newThumb);
        });
        
        // Hide fallback container
        fallbackContainer.style.display = 'none';
        console.log('Fallback thumbnails setup complete');
    }
}

// Test function to check if API endpoint is accessible
async function testAPIEndpoint() {
    console.log('Testing API endpoint...');
    try {
        const response = await fetch('/api/products/random/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        console.log('API test response status:', response.status);
        console.log('API test response headers:', response.headers);
    } catch (error) {
        console.error('API test error:', error);
    }
}

// Image Gallery Functions
function setupImageGallery() {
    console.log('Setting up image gallery');
    const mainImage = document.getElementById('mainImage');
    const thumbnailContainer = document.getElementById('thumbnailContainer');
    
    if (!mainImage || !thumbnailContainer) {
        console.log('Image gallery elements not found');
        return;
    }

    // Get all images from the product data
    const productImagesData = document.getElementById('productImagesData');
    if (!productImagesData) {
        console.log('Product images data element not found');
        return;
    }

    try {
        const allImages = JSON.parse(productImagesData.textContent);
        console.log('Parsed images:', allImages);
        
        if (!allImages || allImages.length === 0) {
            console.log('No images found');
            return;
        }

        // Create thumbnails
        allImages.forEach((img, index) => {
            const thumbnail = document.createElement('img');
            thumbnail.src = img.image;
            thumbnail.alt = `Product Image ${img.order}`;
            thumbnail.className = `thumbnail ${index === 0 ? 'active' : ''}`;
            thumbnail.onclick = () => switchMainImage(img.image, index);
            thumbnailContainer.appendChild(thumbnail);
        });
        console.log('Image gallery setup complete');
    } catch (error) {
        console.error('Error setting up image gallery:', error);
    }
}

function switchMainImage(imageSrc, index) {
    const mainImage = document.getElementById('mainImage');
    const thumbnails = document.querySelectorAll('.thumbnail');
    
    if (mainImage) {
        mainImage.src = imageSrc;
    }
    
    // Update active thumbnail
    thumbnails.forEach((thumb, i) => {
        thumb.classList.toggle('active', i === index);
    });
}

// Cart Functions
function handleAddToCart(event, productId) {
    event.preventDefault(); 
    event.stopPropagation(); // Prevent event from bubbling up to parent div
    console.log('handleAddToCart called with productId:', productId);
    const accessToken = localStorage.getItem('access');
    const guestToken = localStorage.getItem('guest_token');
    console.log('Access token:', accessToken ? 'Present' : 'Not found');
    console.log('Guest token:', guestToken ? 'Present' : 'Not found');

    if (accessToken) {
        // User is already logged in, add directly to cart
        addProductToCart(event, productId);
    } else if (guestToken) {
        // User has guest token, add to guest cart
        addToGuestCart(event, productId, guestToken);
    } else {
        // User is not logged in and no guest token, show modal
        showAddToCartModal(productId);
    }
}

// Function to show the add to cart modal
function showAddToCartModal(productId) {
    // Store the product ID for later use
    window.currentProductId = productId;
    
    // Show the modal
    const modal = new bootstrap.Modal(document.getElementById('addToCartModal'));
    modal.show();
}

// Function to add product to guest cart (for guest users)
function addToGuestCart(event, productId, guestToken) {
    event.stopPropagation(); // Prevent event from bubbling up to parent div
    // Show loading state
    const button = event.target;
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fa fa-spinner fa-spin me-2"></i>Adding...';
    button.style.pointerEvents = 'none';

    // Make API call to add product to guest cart
    console.log('Making API call to /api/cart/guest/add/ with product_id:', productId);
    fetch('/api/cart/guest/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Guest-Token': guestToken,
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            product_id: productId,
            guest_token: guestToken
        })
    })
    .then(response => {
        console.log('Response status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('Response data:', data);
        // Restore button state
        button.innerHTML = originalText;
        button.style.pointerEvents = 'auto';

        if (data.message) {
            window.notificationManager.success(data.message);
        } else {
            window.notificationManager.success('Product added to cart successfully!');
        }
        // Update cart badge after successful addition
        updateCartBadge();
    })
    .catch(error => {
        console.error('Error adding to guest cart:', error);
        // Restore button state
        button.innerHTML = originalText;
        button.style.pointerEvents = 'auto';
        
        window.notificationManager.error('Failed to add product to cart. Please try again.');
    });
}

// Function to add product to cart (for logged-in users)
function addProductToCart(event, productId) {
    event.stopPropagation(); // Prevent event from bubbling up to parent div
    // Show loading state
    const button = event.target;
    const originalText = button.innerHTML;
    button.innerHTML = '<i class="fa fa-spinner fa-spin me-2"></i>Adding...';
    button.style.pointerEvents = 'none';

    // Make API call to add product to cart
    console.log('Making API call to /api/cart/add/ with product_id:', productId);
    fetch('/api/cart/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'Authorization': `Bearer ${localStorage.getItem('access')}`,
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            product_id: productId
        })
    })
    .then(response => {
        console.log('Response status:', response.status);
        return response.json();
    })
    .then(data => {
        console.log('Response data:', data);
        // Restore button state
        button.innerHTML = originalText;
        button.style.pointerEvents = 'auto';

        if (data.message) {
            window.notificationManager.success(data.message);
        } else {
            window.notificationManager.success('Product added to cart successfully!');
        }
        // Update cart badge after successful addition
        updateCartBadge();
    })
    .catch(error => {
        console.error('Error adding to cart:', error);
        // Restore button state
        button.innerHTML = originalText;
        button.style.pointerEvents = 'auto';
        
        window.notificationManager.error('Failed to add product to cart. Please try again.');
    });
}

// Function to handle guest checkout
function handleGuestCheckout() {
    const productId = window.currentProductId;
    if (!productId) {
        window.notificationManager.error('Product ID not found. Please try again.');
        return;
    }

    // Check if guest token already exists
    const existingGuestToken = localStorage.getItem('guest_token');
    if (existingGuestToken) {
        // Use existing guest token
        addToGuestCartFromModal(productId, existingGuestToken);
    } else {
        // Create new guest user and add to cart
        fetch('/api/cart/guest/create/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCSRFToken()
            }
        })
        .then(response => response.json())
        .then(data => {
            if (data.guest_token) {
                // Store guest token
                localStorage.setItem('guest_token', data.guest_token);
                
                // Add product to guest cart
                addToGuestCartFromModal(productId, data.guest_token);
            } else {
                throw new Error(data.error || 'Failed to create guest session');
            }
        })
        .catch(error => {
            console.error('Error in guest checkout:', error);
            window.notificationManager.error(error.message || 'Failed to add product to cart. Please try again.');
        });
    }
}

// Helper function to add to guest cart from modal
function addToGuestCartFromModal(productId, guestToken) {
    fetch('/api/cart/guest/add/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-Guest-Token': guestToken,
            'X-CSRFToken': getCSRFToken()
        },
        body: JSON.stringify({
            product_id: productId,
            guest_token: guestToken
        })
    })
    .then(response => response.json())
    .then(data => {
        if (data.message) {
            window.notificationManager.success(data.message);
            // Update cart badge
            updateCartBadge();
            // Redirect to cart page
            window.location.href = '/cart/';
        } else {
            throw new Error(data.error || 'Failed to add product to cart');
        }
    })
    .catch(error => {
        console.error('Error adding to guest cart:', error);
        window.notificationManager.error(error.message || 'Failed to add product to cart. Please try again.');
    });
}

// Review Functions
function handleAddReview(event, productId) {
    event.preventDefault();
    console.log('Opening review modal for product:', productId);
    
    // Store product ID for submission
    window.currentProductId = productId;
    
    // Reset form
    document.getElementById('reviewForm').reset();
    
    // Show modal
    const modal = new bootstrap.Modal(document.getElementById('reviewModal'));
    modal.show();
}

async function submitReview() {
    const productId = window.currentProductId;
    if (!productId) {
        window.notificationManager.error('Product ID not found. Please refresh the page.');
        return;
    }

    // Get form data
    const name = document.getElementById('reviewName').value.trim();
    const description = document.getElementById('reviewDescription').value.trim();
    const rating = document.getElementById('reviewRating').value;
    const imageFile = document.getElementById('reviewImage').files[0];
    const whtsappImageFile = document.getElementById('whtsappImage').files[0];

    // Validate required fields
    if (!name || !description || !rating) {
        window.notificationManager.error('Please fill in all required fields.');
        return;
    }

    if (rating < 1 || rating > 5) {
        window.notificationManager.error('Please select a valid rating (1-5).');
        return;
    }

    // Show loading state
    const submitBtn = document.querySelector('#reviewModal .btn-primary');
    if (!submitBtn) {
        console.error('Submit button not found');
        window.notificationManager.error('Submit button not found. Please refresh the page.');
        return;
    }
    
    const submitText = submitBtn.querySelector('.submit-text');
    const loadingText = submitBtn.querySelector('.loading-text');
    
    if (!submitText || !loadingText) {
        console.error('Button text elements not found');
        window.notificationManager.error('Button elements not found. Please refresh the page.');
        return;
    }
    
    submitText.style.display = 'none';
    loadingText.style.display = 'inline';
    submitBtn.disabled = true;

    try {
        // Check if user is logged in
        const accessToken = localStorage.getItem('access');
        if (!accessToken) {
            window.notificationManager.error('You need to login to submit a review. Please login and try again.');
            // Optionally redirect to login page
            setTimeout(() => {
                window.location.href = '/login/';
            }, 2000);
            return;
        }

        // Create FormData for file uploads
        const formData = new FormData();
        formData.append('name', name);
        formData.append('description', description);
        formData.append('rating', rating);
        
        if (imageFile) {
            formData.append('image', imageFile);
        }
        
        if (whtsappImageFile) {
            formData.append('whtsapp_image', whtsappImageFile);
        }

        // Prepare headers
        const headers = {
            'X-CSRFToken': getCSRFToken(),
            'Authorization': `Bearer ${accessToken}`
        };

        // Make API call
        const response = await fetch(`/api/reviews/${productId}/reviews-add/`, {
            method: 'POST',
            body: formData,
            headers: headers
        });

        const data = await response.json();

        if (response.ok) {
            // Success
            if (data.message) {
                window.notificationManager.success(data.message);
            } else {
                window.notificationManager.success('Review submitted successfully!');
            }
            
            // Show additional info if product was activated
            if (data.product_activated) {
                window.notificationManager.info('Product has been activated and is now visible!');
            }
            
            // Close modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('reviewModal'));
            modal.hide();
            
            // Optionally refresh the page to show the new review
            setTimeout(() => {
                window.location.reload();
            }, 1500);
        } else {
            // Handle specific error cases
            let errorMessage = 'Failed to submit review. Please try again.';
            
            if (response.status === 401) {
                // Unauthorized - user not logged in
                errorMessage = 'You need to login to submit a review. Please login and try again.';
                setTimeout(() => {
                    window.location.href = '/login/';
                }, 2000);
            } else if (response.status === 403) {
                // Forbidden - user not eligible
                errorMessage = data.error || data.detail || 'You are not eligible to post a review.';
            } else if (data.error) {
                errorMessage = data.error;
            } else if (data.detail) {
                errorMessage = data.detail;
            } else if (data.message) {
                errorMessage = data.message;
            }
            
            window.notificationManager.error(errorMessage);
        }
    } catch (error) {
        console.error('Error submitting review:', error);
        window.notificationManager.error('Network error. Please check your connection and try again.');
    } finally {
        // Restore button state safely
        if (submitBtn && submitText && loadingText) {
            submitText.style.display = 'inline';
            loadingText.style.display = 'none';
            submitBtn.disabled = false;
        }
    }
}

// Helper Functions
function getCSRFToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : '';
}

async function updateCartBadge() {
    const accessToken = localStorage.getItem('access');
    const cartBadge = document.getElementById('cartBadge');
    
    if (!accessToken || !cartBadge) {
        return;
    }

    try {
        const response = await fetch('/api/cart/', {
            method: 'GET',
            headers: {
                'Authorization': `Bearer ${accessToken}`,
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const cartData = await response.json();
            const totalQuantity = cartData.total_quantity || 0;
            cartBadge.textContent = totalQuantity.toString();
        } else if (response.status === 401) {
            cartBadge.textContent = '0';
        } else {
            cartBadge.textContent = '0';
        }
    } catch (error) {
        console.error('Error updating cart badge:', error);
        cartBadge.textContent = '0';
    }
}

// Quantity Functions
function updateQuantity(change) {
    const quantityInput = document.querySelector('.quantity input');
    let currentQuantity = parseInt(quantityInput.value) || 1;
    currentQuantity = Math.max(1, currentQuantity + change);
    quantityInput.value = currentQuantity;
}

// Random Products Slider Functions
async function loadRandomProducts() {
    console.log('Loading random products...');
    try {
        const response = await fetch('/api/products/random/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        
        console.log('API response status:', response.status);
        
        if (response.ok) {
            const products = await response.json();
            console.log('Random products received:', products);
            renderRandomProducts(products);
            initializeProductCarousel();
        } else {
            console.error('Failed to load random products. Status:', response.status);
            const errorText = await response.text();
            console.error('Error response:', errorText);
        }
    } catch (error) {
        console.error('Error loading random products:', error);
    }
}

function renderRandomProducts(products) {
    const carousel = document.querySelector('.product-carousel');
    if (!carousel) return;

    carousel.innerHTML = products.map(product => `
        <div class="item">
            <div class="rounded position-relative fruite-item h-100">
                <div class="fruite-img" style="height: 200px; overflow: hidden;">
                    <img src="${product.image || '/static/img/fruite-item-1.jpg'}" 
                         class="img-fluid w-100 rounded-top" 
                         style="height: 100%; object-fit: cover;" 
                         alt="${product.name}">
                </div>
                <div class="text-white bg-secondary px-3 py-1 rounded position-absolute" 
                     style="top: 10px; left: 10px;">
                    ${product.product_type ? product.product_type.charAt(0).toUpperCase() + product.product_type.slice(1) : 'Product'}
                </div>
                <div class="p-4 border border-secondary border-top-0 rounded-bottom d-flex flex-column h-100">
                    <h4 class="mb-2">${product.name}</h4>
                    <p class="mb-3 flex-grow-1">${product.description || 'Lorem ipsum dolor sit amet consectetur adipisicing elit sed do eiusmod te incididunt'}</p>
                    <p class="text-dark fs-5 fw-bold mb-0 text-center mb-3">Rs${product.price}</p>
                    <div class="d-flex justify-content-center flex-lg-wrap align-items-center mt-auto mt-3">
                        <a href="/product-detail/${product.id}/" class="btn border border-secondary rounded-pill px-3 text-primary">
                            <i class="fa fa-eye me-2 text-primary"></i> View Details
                        </a>
                    </div>
                </div>
            </div>
        </div>
    `).join('');
}

function initializeProductCarousel() {
    const carousel = document.querySelector('.product-carousel');
    if (!carousel) return;

    // Initialize Owl Carousel
    $(carousel).owlCarousel({
        loop: true,
        margin: 20,
        nav: true,
        responsive: {
            0: {
                items: 1
            },
            576: {
                items: 2
            },
            768: {
                items: 2
            },
            992: {
                items: 3
            }
        },
        navText: [
            '<i class="fa fa-chevron-left"></i>',
            '<i class="fa fa-chevron-right"></i>'
        ]
    });
}

// Modal event listeners
document.addEventListener('DOMContentLoaded', function() {
    // Google Login button
    const googleLoginBtn = document.getElementById('googleLoginBtn');
    if (googleLoginBtn) {
        googleLoginBtn.addEventListener('click', function() {
            // Hide modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('addToCartModal'));
            modal.hide();
            
            // Get Google OAuth URL and redirect
            fetch('/accounts/google-oauth-initiate/')
                .then(response => response.json())
                .then(data => {
                    if (data.auth_url) {
                        window.location.href = data.auth_url;
                    } else {
                        window.notificationManager.error('Failed to initiate Google login. Please try again.');
                    }
                })
                .catch(error => {
                    console.error('Error initiating Google login:', error);
                    window.notificationManager.error('Failed to initiate Google login. Please try again.');
                });
        });
    }

    // Continue as Guest button
    const continueAsGuestBtn = document.getElementById('continueAsGuestBtn');
    if (continueAsGuestBtn) {
        continueAsGuestBtn.addEventListener('click', function() {
            // Hide modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('addToCartModal'));
            modal.hide();
            
            // Handle guest checkout
            handleGuestCheckout();
        });
    }
});

// Export functions for global access
window.handleAddToCart = handleAddToCart;
window.updateQuantity = updateQuantity;
window.switchMainImage = switchMainImage;
window.handleAddReview = handleAddReview;
window.submitReview = submitReview;
