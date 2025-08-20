// Shop Page JavaScript
// Handles filtering, pagination, and other shop-specific functionality

// Function to set price range from quick buttons
function setPriceRange(min, max) {
    document.getElementById('minPrice').value = min;
    if (max === 1000) {
        document.getElementById('maxPrice').value = ''; // No upper limit for Rs500+
    } else {
        document.getElementById('maxPrice').value = max;
    }
    // Auto-submit the form
    document.getElementById('priceFilterForm').submit();
}

// Function to clear all filters
function clearAllFilters() {
    // Get the current page path without query parameters
    const currentPath = window.location.pathname;
    window.location.href = currentPath;
}

// Function to preserve filters in pagination links
function updatePaginationLinks() {
    const currentUrl = new URL(window.location);
    const searchParams = currentUrl.searchParams;
    
    // Get current filter values
    const search = searchParams.get('search') || '';
    const category = searchParams.get('category') || '';
    const minPrice = searchParams.get('min_price') || '';
    const maxPrice = searchParams.get('max_price') || '';
    
    // Update all pagination links to preserve filters
    const paginationLinks = document.querySelectorAll('.pagination a');
    paginationLinks.forEach(link => {
        const linkUrl = new URL(link.href);
        if (search) linkUrl.searchParams.set('search', search);
        if (category) linkUrl.searchParams.set('category', category);
        if (minPrice) linkUrl.searchParams.set('min_price', minPrice);
        if (maxPrice) linkUrl.searchParams.set('max_price', maxPrice);
        link.href = linkUrl.toString();
    });
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    updatePaginationLinks();
    
    // Add event listeners for price filter form
    const priceForm = document.getElementById('priceFilterForm');
    if (priceForm) {
        priceForm.addEventListener('submit', function(e) {
            // Validate price inputs
            const minPrice = document.getElementById('minPrice').value;
            const maxPrice = document.getElementById('maxPrice').value;
            
            if (minPrice && maxPrice && parseFloat(minPrice) > parseFloat(maxPrice)) {
                e.preventDefault();
                alert('Minimum price cannot be greater than maximum price');
                return false;
            }
        });
    }
});

// Export functions for global access
window.setPriceRange = setPriceRange;
window.clearAllFilters = clearAllFilters;
