// Product Detail Page JavaScript
// Handles image gallery, cart functionality, and other product-specific features

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    setupImageGallery();
    loadRandomProducts();
});

// Image Gallery Functions
function setupImageGallery() {
    const mainImage = document.getElementById('mainImage');
    const thumbnailContainer = document.getElementById('thumbnailContainer');
    
    if (!mainImage || !thumbnailContainer) return;

    // Get all images from the product data
    const allImages = JSON.parse(document.getElementById('productImagesData').textContent);
    
    if (!allImages || allImages.length === 0) return;

    // Create thumbnails
    allImages.forEach((img, index) => {
        const thumbnail = document.createElement('img');
        thumbnail.src = img.image;
        thumbnail.alt = `Product Image ${img.order}`;
        thumbnail.className = `thumbnail ${index === 0 ? 'active' : ''}`;
        thumbnail.onclick = () => switchMainImage(img.image, index);
        thumbnailContainer.appendChild(thumbnail);
    });
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
    console.log('handleAddToCart called with productId:', productId);
    const accessToken = localStorage.getItem('access');
    console.log('Access token:', accessToken ? 'Present' : 'Not found');

    if (accessToken) {
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
                'Authorization': `Bearer ${accessToken}`,
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
    } else {
        window.notificationManager.warning('Please log in to add items to your cart.');
        setTimeout(() => {
            window.location.href = '/login/';
        }, 2000);
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
    try {
        const response = await fetch('/api/products/random/', {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });

        if (response.ok) {
            const products = await response.json();
            renderRandomProducts(products);
            initializeProductCarousel();
        } else {
            console.error('Failed to load random products');
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
                    <div class="d-flex justify-content-between flex-lg-wrap align-items-center mt-auto">
                        <p class="text-dark fs-5 fw-bold mb-0">Rs${product.price}</p>
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
                items: 3
            },
            992: {
                items: 4
            }
        },
        navText: [
            '<i class="fa fa-chevron-left"></i>',
            '<i class="fa fa-chevron-right"></i>'
        ]
    });
}

// Export functions for global access
window.handleAddToCart = handleAddToCart;
window.updateQuantity = updateQuantity;
window.switchMainImage = switchMainImage;
