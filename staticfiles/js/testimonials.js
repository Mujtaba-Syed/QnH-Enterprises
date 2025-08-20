// Testimonials Page JavaScript
// Handles loading testimonials from API and frontend pagination

class TestimonialsManager {
    constructor() {
        this.testimonials = [];
        this.currentPage = 1;
        this.itemsPerPage = 9; // 3x3 grid
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
        
        let paginationHTML = '';
        
        // Previous button
        if (this.currentPage > 1) {
            paginationHTML += `
                <li class="page-item">
                    <a class="page-link" href="#" onclick="testimonialsManager.goToPage(${this.currentPage - 1}); return false;">Previous</a>
                </li>
            `;
        }
        
        // Page numbers
        const startPage = Math.max(1, this.currentPage - 2);
        const endPage = Math.min(totalPages, this.currentPage + 2);
        
        for (let i = startPage; i <= endPage; i++) {
            if (i === this.currentPage) {
                paginationHTML += `
                    <li class="page-item active">
                        <span class="page-link">${i}</span>
                    </li>
                `;
            } else {
                paginationHTML += `
                    <li class="page-item">
                        <a class="page-link" href="#" onclick="testimonialsManager.goToPage(${i}); return false;">${i}</a>
                    </li>
                `;
            }
        }
        
        // Next button
        if (this.currentPage < totalPages) {
            paginationHTML += `
                <li class="page-item">
                    <a class="page-link" href="#" onclick="testimonialsManager.goToPage(${this.currentPage + 1}); return false;">Next</a>
                </li>
            `;
        }
        
        this.paginationList.innerHTML = paginationHTML;
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
