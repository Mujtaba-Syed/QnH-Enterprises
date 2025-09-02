class CartManager {
    constructor() {
        this.cartItems = [];
        this.baseUrl = '/api/cart/';
        this.init();
    }

    async init() {
        const accessToken = localStorage.getItem('access');
        const guestToken = localStorage.getItem('guest_token');
        
        if (!accessToken && !guestToken) {
            window.location.href = '/login/';
            return;
        }
        
        await this.loadCart();
        this.setupEventListeners();
    }

    getAuthHeaders() {
        const accessToken = localStorage.getItem('access');
        const guestToken = localStorage.getItem('guest_token');
        const headers = {
            'Content-Type': 'application/json',
            'X-CSRFToken': this.getCSRFToken()
        };
        
        if (accessToken) {
            headers['Authorization'] = `Bearer ${accessToken}`;
        } else if (guestToken) {
            headers['X-Guest-Token'] = guestToken;
        }
        
        return headers;
    }

    async loadCart() {
        try {
            const accessToken = localStorage.getItem('access');
            const guestToken = localStorage.getItem('guest_token');
            console.log('Loading cart with token:', accessToken ? 'User token' : guestToken ? 'Guest token' : 'No token');
            
            // Determine which endpoint to use
            const url = accessToken ? this.baseUrl : `${this.baseUrl}guest/`;
            
            const response = await fetch(url, {
                method: 'GET',
                headers: this.getAuthHeaders()
            });

            console.log('Cart API response status:', response.status);

            if (response.ok) {
                const cartData = await response.json();
                console.log('Cart data received:', cartData);
                this.cartItems = cartData.items || [];
                this.renderCart();
                this.updateNavbarCartBadge(cartData.total_quantity || 0);
            } else if (response.status === 401) {
                console.log('Unauthorized - redirecting to login');
                // User not authenticated, redirect to login
                window.location.href = '/login/';
            } else if (response.status === 404) {
                console.log('Cart not found - showing empty cart');
                // Cart not found, show empty cart
                this.cartItems = [];
                this.renderCart();
                this.updateNavbarCartBadge(0);
            } else {
                const errorText = await response.text();
                console.error('Failed to load cart:', response.status, errorText);
                this.showMessage('Failed to load cart items', 'error');
            }
        } catch (error) {
            console.error('Error loading cart:', error);
            this.showMessage('Error loading cart items', 'error');
        }
    }

    updateNavbarCartBadge(count) {
        const cartBadge = document.getElementById('cartBadge');
        if (cartBadge) {
            cartBadge.textContent = count.toString();
        }
    }

    renderCart() {
        const tbody = document.querySelector('.table tbody');
        const subtotalElement = document.querySelector('.subtotal-value');
        const totalElement = document.querySelector('.total-value');
        const itemCountElement = document.querySelector('.item-count');

        if (this.cartItems.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="6" class="text-center py-5">
                        <img src="/static/img/vegetable-item-5.jpg" class="img-fluid mb-3" style="width: 100px; height: 100px; opacity: 0.5;" alt="Empty Cart">
                        <h5>Your cart is empty</h5>
                        <p class="text-muted">Add some products to your cart to get started!</p>
                        <a href="/shop/" class="btn btn-primary">Continue Shopping</a>
                    </td>
                </tr>
            `;
            if (subtotalElement) subtotalElement.textContent = '$0.00';
            if (totalElement) totalElement.textContent = '$0.00';
            if (itemCountElement) itemCountElement.textContent = '0';
            return;
        }

        tbody.innerHTML = this.cartItems.map(item => this.renderCartItem(item)).join('');
        
        // Update totals
        const subtotal = this.calculateSubtotal();
        const shipping = 3.00; // Flat rate shipping
        const total = subtotal + shipping;

        if (subtotalElement) subtotalElement.textContent = `Rs.${subtotal.toFixed(2)}`;
        if (totalElement) totalElement.textContent = `Rs.${total.toFixed(2)}`;
        if (itemCountElement) itemCountElement.textContent = this.cartItems.length.toString();
    }

    renderCartItem(item) {
        const imageUrl = item.product.image ? item.product.image : '/static/img/vegetable-item-5.jpg';
        return `
            <tr data-product-id="${item.product.id}">
                <th scope="row">
                    <div class="d-flex align-items-center">
                        <img src="${imageUrl}" class="img-fluid me-5 rounded-circle" style="width: 80px; height: 80px;" alt="${item.product.name}" onerror="this.src='/static/img/vegetable-item-5.jpg'">
                    </div>
                </th>
                <td>
                    <p class="mb-0 mt-4">${item.product.name}</p>
                </td>
                <td>
                    <p class="mb-0 mt-4">Rs.${item.product.price}</p>
                </td>
                <td>
                    <div class="input-group quantity mt-4" style="width: 100px;">
                        <div class="input-group-btn">
                            <button class="btn btn-sm btn-minus rounded-circle bg-light border" data-product-id="${item.product.id}">
                                <i class="fa fa-minus"></i>
                            </button>
                        </div>
                        <input type="text" class="form-control form-control-sm text-center border-0 quantity-input" value="${item.quantity}" data-product-id="${item.product.id}" readonly>
                        <div class="input-group-btn">
                            <button class="btn btn-sm btn-plus rounded-circle bg-light border" data-product-id="${item.product.id}">
                                <i class="fa fa-plus"></i>
                            </button>
                        </div>
                    </div>
                </td>
                <td>
                    <p class="mb-0 mt-4 item-total" data-product-id="${item.product.id}">Rs.${item.total}</p>
                </td>
                <td>
                    <button class="btn btn-md rounded-circle bg-light border mt-4 remove-item" data-product-id="${item.product.id}">
                        <i class="fa fa-times text-danger"></i>
                    </button>
                </td>
            </tr>
        `;
    }

    setupEventListeners() {
        // Delegate events to handle dynamically added elements
        document.addEventListener('click', (e) => {
            if (e.target.closest('.btn-plus')) {
                const productId = e.target.closest('.btn-plus').dataset.productId;
                this.increaseQuantity(productId);
            } else if (e.target.closest('.btn-minus')) {
                const productId = e.target.closest('.btn-minus').dataset.productId;
                this.decreaseQuantity(productId);
            } else if (e.target.closest('.remove-item')) {
                const productId = e.target.closest('.remove-item').dataset.productId;
                this.removeItem(productId);
            }
        });

        // Checkout button
        const checkoutBtn = document.getElementById('checkout-button');
        if (checkoutBtn) {
            checkoutBtn.addEventListener('click', () => {
                if (this.cartItems.length > 0) {
                    window.location.href = '/checkout/';
                } else {
                    this.showMessage('Your cart is empty', 'warning');
                }
            });
        }

        // Apply coupon button
        const applyCouponBtn = document.querySelector('.apply-coupon-btn');
        if (applyCouponBtn) {
            applyCouponBtn.addEventListener('click', () => {
                this.applyCoupon();
            });
        }

        // Clear cart button
        const clearCartBtn = document.querySelector('.clear-cart-btn');
        if (clearCartBtn) {
            clearCartBtn.addEventListener('click', () => {
                this.clearCart();
            });
        }
    }

    async increaseQuantity(productId) {
        try {
            const accessToken = localStorage.getItem('access');
            const guestToken = localStorage.getItem('guest_token');
            
            if (guestToken && !accessToken) {
                // Guest user - add item to guest cart
                const response = await fetch(`${this.baseUrl}guest/add/`, {
                    method: 'POST',
                    headers: this.getAuthHeaders(),
                    body: JSON.stringify({
                        product_id: productId,
                        guest_token: guestToken
                    })
                });

                if (response.ok) {
                    await this.loadCart();
                    this.showMessage('Quantity updated successfully', 'success');
                } else {
                    const error = await response.json();
                    this.showMessage(error.error || 'Failed to update quantity', 'error');
                }
            } else {
                // Authenticated user - use regular endpoint
                const response = await fetch(`${this.baseUrl}update/${productId}/`, {
                    method: 'PUT',
                    headers: this.getAuthHeaders()
                });

                if (response.ok) {
                    await this.loadCart();
                    this.showMessage('Quantity updated successfully', 'success');
                } else {
                    const error = await response.json();
                    this.showMessage(error.error || 'Failed to update quantity', 'error');
                }
            }
        } catch (error) {
            console.error('Error increasing quantity:', error);
            this.showMessage('Error updating quantity', 'error');
        }
    }

    async decreaseQuantity(productId) {
        try {
            const accessToken = localStorage.getItem('access');
            const guestToken = localStorage.getItem('guest_token');
            
            if (guestToken && !accessToken) {
                // Guest user - use guest decrease endpoint
                const response = await fetch(`${this.baseUrl}guest/decrease/${productId}/`, {
                    method: 'PUT',
                    headers: this.getAuthHeaders()
                });

                if (response.ok) {
                    await this.loadCart();
                    this.showMessage('Quantity updated successfully', 'success');
                } else {
                    const error = await response.json();
                    this.showMessage(error.error || 'Failed to update quantity', 'error');
                }
            } else {
                // Authenticated user - use regular endpoint
                const response = await fetch(`${this.baseUrl}decrease/${productId}/`, {
                    method: 'PUT',
                    headers: this.getAuthHeaders()
                });

                if (response.ok) {
                    await this.loadCart();
                    this.showMessage('Quantity updated successfully', 'success');
                } else {
                    const error = await response.json();
                    this.showMessage(error.error || 'Failed to update quantity', 'error');
                }
            }
        } catch (error) {
            console.error('Error decreasing quantity:', error);
            this.showMessage('Error updating quantity', 'error');
        }
    }

    async removeItem(productId) {
        // Use custom confirmation notification instead of browser alert
        if (window.notificationManager) {
            window.notificationManager.confirm(
                'Are you sure you want to remove this item from your cart?',
                async () => {
                    // User confirmed - proceed with removal
                    await this.performRemoveItem(productId);
                },
                () => {
                    // User cancelled - do nothing
                    console.log('Item removal cancelled by user');
                }
            );
        } else {
            // Fallback to browser confirm if notification manager is not available
            if (!confirm('Are you sure you want to remove this item from your cart?')) {
                return;
            }
            await this.performRemoveItem(productId);
        }
    }

    async performRemoveItem(productId) {
        try {
            const accessToken = localStorage.getItem('access');
            const guestToken = localStorage.getItem('guest_token');
            
            if (guestToken && !accessToken) {
                // Guest user - use guest remove endpoint
                const response = await fetch(`${this.baseUrl}guest/remove/${productId}/`, {
                    method: 'DELETE',
                    headers: this.getAuthHeaders()
                });

                if (response.ok) {
                    await this.loadCart();
                    this.showMessage('Item removed from cart', 'success');
                } else {
                    const error = await response.json();
                    this.showMessage(error.error || 'Failed to remove item', 'error');
                }
            } else {
                // Authenticated user - use regular endpoint
                const response = await fetch(`${this.baseUrl}remove/${productId}/`, {
                    method: 'DELETE',
                    headers: this.getAuthHeaders()
                });

                if (response.ok) {
                    await this.loadCart();
                    this.showMessage('Item removed from cart', 'success');
                } else {
                    const error = await response.json();
                    this.showMessage(error.error || 'Failed to remove item', 'error');
                }
            }
        } catch (error) {
            console.error('Error removing item:', error);
            this.showMessage('Error removing item', 'error');
        }
    }

    async clearCart() {
        // Use custom confirmation notification instead of browser alert
        if (window.notificationManager) {
            window.notificationManager.confirm(
                'Are you sure you want to clear your entire cart?',
                async () => {
                    // User confirmed - proceed with clearing
                    await this.performClearCart();
                },
                () => {
                    // User cancelled - do nothing
                    console.log('Cart clearing cancelled by user');
                }
            );
        } else {
            // Fallback to browser confirm if notification manager is not available
            if (!confirm('Are you sure you want to clear your entire cart?')) {
                return;
            }
            await this.performClearCart();
        }
    }

    async performClearCart() {
        try {
            const response = await fetch(`${this.baseUrl}clear/`, {
                method: 'DELETE',
                headers: this.getAuthHeaders()
            });

            if (response.ok) {
                await this.loadCart();
                this.showMessage('Cart cleared successfully', 'success');
            } else {
                const error = await response.json();
                this.showMessage(error.error || 'Failed to clear cart', 'error');
            }
        } catch (error) {
            console.error('Error clearing cart:', error);
            this.showMessage('Error clearing cart', 'error');
        }
    }

    applyCoupon() {
        const couponInput = document.querySelector('input[placeholder="Coupon Code"]');
        const couponCode = couponInput ? couponInput.value.trim() : '';
        
        if (!couponCode) {
            this.showMessage('Please enter a coupon code', 'warning');
            return;
        }

        // TODO: Implement coupon logic
        this.showMessage('Coupon functionality coming soon!', 'info');
    }

    calculateSubtotal() {
        return this.cartItems.reduce((total, item) => {
            return total + (parseFloat(item.product.price) * item.quantity);
        }, 0);
    }

    getCSRFToken() {
        const token = document.querySelector('[name=csrfmiddlewaretoken]');
        return token ? token.value : '';
    }

    showMessage(message, type = 'info') {
        // Use the new notification system
        if (window.notificationManager) {
            window.notificationManager.show(message, type, 4000);
        } else {
            // Fallback to simple alert if notification system is not available
            alert(message);
        }
    }
}

// Initialize cart when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Only initialize cart if user is authenticated (cart table exists)
    const cartTable = document.querySelector('.table');
    if (cartTable) {
        window.cartManager = new CartManager();
    }
}); 