// Testimonials Page JavaScript
// Handles loading testimonials from API and frontend pagination

class TestimonialsManager {
    constructor() {
        this.testimonials = [];
        this.currentPage = 1;
        this.itemsPerPage = 6; // 2x3 grid
        this.container = document.getElementById('testimonialsContainer');
        this.paginationContainer = document.getElementById('paginationContainer');
        this.paginationList = document.getElementById('paginationList');
        this.loadingSpinner = document.getElementById('loadingSpinner');
        
        this.init();
    }
    
    async init() {
        await this.loadTestimonials();
        this.renderTestimonials();
        this.renderPagination();
    }
    
    async loadTestimonials() {
        try {
            this.showLoading();
            
            // Load all testimonials from the API
            const response = await fetch('/api/reviews/active-reviews/', {
                method: 'GET',
                headers: {
                    'Content-Type': 'application/json'
                }
            });
            
            if (response.ok) {
                this.testimonials = await response.json();
                console.log('Loaded testimonials:', this.testimonials);
            } else {
                console.error('Failed to load testimonials:', response.status);
                this.testimonials = [];
            }
        } catch (error) {
            console.error('Error loading testimonials:', error);
            this.testimonials = [];
        } finally {
            this.hideLoading();
        }
    }
    
    showLoading() {
        if (this.loadingSpinner) {
            this.loadingSpinner.style.display = 'block';
        }
        if (this.container) {
            this.container.style.display = 'none';
        }
        if (this.paginationContainer) {
            this.paginationContainer.style.display = 'none';
        }
    }
    
    hideLoading() {
        if (this.loadingSpinner) {
            this.loadingSpinner.style.display = 'none';
        }
        if (this.container) {
            this.container.style.display = 'flex';
        }
    }
    
    renderTestimonials() {
        if (!this.container) return;
        
        const startIndex = (this.currentPage - 1) * this.itemsPerPage;
        const endIndex = startIndex + this.itemsPerPage;
        const pageTestimonials = this.testimonials.slice(startIndex, endIndex);
        
        if (pageTestimonials.length === 0) {
            this.container.innerHTML = `
                <div class="col-12 text-center py-5">
                    <i class="fa fa-comments fa-3x text-muted mb-3"></i>
                    <h5 class="text-muted">No testimonials found</h5>
                    <p class="text-muted">Be the first to leave a review!</p>
                </div>
            `;
            return;
        }
        
        this.container.innerHTML = pageTestimonials.map(review => `
            <div class="col-lg-4 col-md-6 col-sm-12">
                <div class="card h-100 shadow-sm border-0">
                    <div class="card-body p-4">
                        <!-- Quote Icon -->
                        <div class="text-end mb-3">
                            <i class="fa fa-quote-right fa-2x text-secondary"></i>
                        </div>
                        
                        <!-- Review Text -->
                        <div class="mb-4">
                            <p class="card-text text-muted">${this.truncateText(review.description, 150)}</p>
                        </div>
                        
                        <!-- Rating Stars -->
                        <div class="mb-3">
                            ${this.generateStars(review.rating)}
                        </div>
                        
                        <!-- Client Info -->
                        <div class="d-flex align-items-center">
                            <div class="me-3">
                                ${this.generateProfileImage(review)}
                            </div>
                            <div>
                                <h6 class="card-title mb-1 fw-bold">${review.name}</h6>
                                <small class="text-muted">Client</small>
                            </div>
                        </div>
                    </div>
                </div>
            </div>
        `).join('');
    }
    
    generateStars(rating) {
        let stars = '';
        for (let i = 1; i <= 5; i++) {
            if (i <= rating) {
                stars += '<i class="fas fa-star text-warning"></i>';
            } else {
                stars += '<i class="fas fa-star text-muted"></i>';
            }
        }
        return stars;
    }
    
    generateProfileImage(review) {
        if (review.image) {
            return `<img src="${review.image}" class="rounded-circle" style="width: 60px; height: 60px; object-fit: cover;" alt="${review.name}">`;
        } else {
            return `<div class="rounded-circle bg-secondary d-flex align-items-center justify-content-center" style="width: 60px; height: 60px;">
                        <i class="fa fa-user text-white"></i>
                    </div>`;
        }
    }
    
    truncateText(text, maxLength) {
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength) + '...';
    }
    
    renderPagination() {
        if (!this.paginationContainer || !this.paginationList) return;
        
        const totalPages = Math.ceil(this.testimonials.length / this.itemsPerPage);
        
        if (totalPages <= 1) {
            this.paginationContainer.style.display = 'none';
            return;
        }
        
        this.paginationContainer.style.display = 'block';
        
        // Ensure proper Bootstrap classes
        this.paginationContainer.className = 'd-flex justify-content-center';
        this.paginationList.className = 'pagination justify-content-center align-items-center mb-0';
        
        let paginationHTML = '';
        
        // First Page Button (<<)
        if (this.currentPage > 1) {
            paginationHTML += `
                <li class="page-item">
                    <a class="page-link border-0 rounded-pill px-3 py-2 me-2" style="background-color: #e8f5e8; border-color: #198754; color: #198754; transition: all 0.3s ease;" 
                       onmouseover="this.style.backgroundColor='#198754'; this.style.color='white';" 
                       onmouseout="this.style.backgroundColor='#e8f5e8'; this.style.color='#198754';" 
                       href="#" onclick="testimonialsManager.goToPage(1); return false;" title="First Page">
                        <i class="fa fa-angle-double-left"></i>
                    </a>
                </li>
            `;
        }
        
        // Previous Page Button (<)
        if (this.currentPage > 1) {
            paginationHTML += `
                <li class="page-item">
                    <a class="page-link border-0 rounded-pill px-3 py-2 me-3" style="background-color: #e8f5e8; border-color: #198754; color: #198754; transition: all 0.3s ease;" 
                       onmouseover="this.style.backgroundColor='#198754'; this.style.color='white';" 
                       onmouseout="this.style.backgroundColor='#e8f5e8'; this.style.color='#198754';" 
                       href="#" onclick="testimonialsManager.goToPage(${this.currentPage - 1}); return false;" title="Previous Page">
                        <i class="fa fa-angle-left"></i>
                    </a>
                </li>
            `;
        }
        
        // Page Numbers (centered horizontally)
        const startPage = Math.max(1, this.currentPage - 2);
        const endPage = Math.min(totalPages, this.currentPage + 2);
        
        // Add spacing before page numbers if needed
        if (startPage > 1) {
            paginationHTML += `<li class="page-item me-2"><span class="page-link border-0 text-muted">...</span></li>`;
        }
        
        for (let i = startPage; i <= endPage; i++) {
            if (i === this.currentPage) {
                paginationHTML += `
                    <li class="page-item mx-1">
                        <span class="page-link border-0 rounded-pill px-3 py-2" style="background-color: #ffb524; border-color: #ffb524; color: white; font-weight: bold;">${i}</span>
                    </li>
                `;
            } else {
                paginationHTML += `
                    <li class="page-item mx-1">
                        <a class="page-link border rounded-pill px-3 py-2" style="background-color: white; border-color: #198754; color: #198754; transition: all 0.3s ease;" 
                           onmouseover="this.style.backgroundColor='#198754'; this.style.color='white';" 
                           onmouseout="this.style.backgroundColor='white'; this.style.color='#198754';" 
                           href="#" onclick="testimonialsManager.goToPage(${i}); return false;">${i}</a>
                    </li>
                `;
            }
        }
        
        // Add spacing after page numbers if needed
        if (endPage < totalPages) {
            paginationHTML += `<li class="page-item ms-2"><span class="page-link border-0 text-muted">...</span></li>`;
        }
        
        // Next Page Button (>)
        if (this.currentPage < totalPages) {
            paginationHTML += `
                <li class="page-item">
                    <a class="page-link border-0 rounded-pill px-3 py-2 ms-3" style="background-color: #e8f5e8; border-color: #198754; color: #198754; transition: all 0.3s ease;" 
                       onmouseover="this.style.backgroundColor='#198754'; this.style.color='white';" 
                       onmouseout="this.style.backgroundColor='#e8f5e8'; this.style.color='#198754';" 
                       href="#" onclick="testimonialsManager.goToPage(${this.currentPage + 1}); return false;" title="Next Page">
                        <i class="fa fa-angle-right"></i>
                    </a>
                </li>
            `;
        }
        
        // Last Page Button (>>)
        if (this.currentPage < totalPages) {
            paginationHTML += `
                <li class="page-item">
                    <a class="page-link border-0 rounded-pill px-3 py-2 ms-2" style="background-color: #e8f5e8; border-color: #198754; color: #198754; transition: all 0.3s ease;" 
                       onmouseover="this.style.backgroundColor='#198754'; this.style.color='white';" 
                       onmouseout="this.style.backgroundColor='#e8f5e8'; this.style.color='#198754';" 
                       href="#" onclick="testimonialsManager.goToPage(${totalPages}); return false;" title="Last Page">
                        <i class="fa fa-angle-double-right"></i>
                    </a>
                </li>
            `;
        }
        
        this.paginationList.innerHTML = paginationHTML;
        
        // Add custom CSS for better pagination appearance
        this.addPaginationStyles();
        
        // Debug info
        console.log('Pagination rendered with', totalPages, 'pages');
        console.log('Current page:', this.currentPage);
    }
    
    addPaginationStyles() {
        // Add custom styles for better pagination appearance
        const style = document.createElement('style');
        style.textContent = `
            .pagination {
                display: flex !important;
                flex-direction: row !important;
                justify-content: center !important;
                align-items: center !important;
                flex-wrap: nowrap !important;
                gap: 8px;
                margin: 0;
                padding: 0;
                list-style: none;
            }
            
            .pagination .page-item {
                display: inline-block;
                margin: 0;
                padding: 0;
            }
            
            .pagination .page-link {
                transition: all 0.3s ease;
                font-weight: 500;
                min-width: 45px;
                text-align: center;
                display: flex;
                align-items: center;
                justify-content: center;
                height: 45px;
                text-decoration: none;
                border-radius: 25px;
                padding: 8px 16px;
                margin: 0;
            }
            
            .pagination .page-link:hover {
                transform: translateY(-2px);
                box-shadow: 0 4px 8px rgba(0,0,0,0.1);
                text-decoration: none;
            }
            
            .pagination .page-item.active .page-link {
                box-shadow: 0 4px 12px rgba(13, 110, 253, 0.3);
            }
            
            .pagination .page-item:not(.active) .page-link:hover {
                background-color: #f8f9fa;
                border-color: #6c757d;
                color: #495057;
            }
            
            .pagination .page-link:focus {
                box-shadow: 0 0 0 0.2rem rgba(13, 110, 253, 0.25);
                outline: none;
            }
            
            .pagination .page-item .text-muted {
                background: transparent;
                border: none;
                pointer-events: none;
                color: #6c757d !important;
            }
            
            .pagination .page-item .text-muted:hover {
                transform: none;
                box-shadow: none;
                background: transparent !important;
            }
            
            /* Force horizontal layout */
            .pagination li {
                float: left !important;
                display: inline-block !important;
            }
            
            /* Ensure container is centered */
            #paginationContainer {
                text-align: center;
                width: 100%;
            }
            
            #paginationList {
                display: inline-flex !important;
                flex-direction: row !important;
                justify-content: center !important;
                align-items: center !important;
                margin: 0 auto;
                padding: 0;
            }
        `;
        
        if (!document.getElementById('paginationStyles')) {
            style.id = 'paginationStyles';
            document.head.appendChild(style);
        }
    }
    
    goToPage(page) {
        this.currentPage = page;
        this.renderTestimonials();
        this.renderPagination();
        
        // Scroll to top of testimonials
        this.container.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Initialize when page loads
document.addEventListener('DOMContentLoaded', function() {
    window.testimonialsManager = new TestimonialsManager();
});
