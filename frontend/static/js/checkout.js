class CheckoutManager {
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
            console.log('Loading cart for checkout with token:', accessToken ? 'User token' : guestToken ? 'Guest token' : 'No token');
            
            // Determine which endpoint to use
            const url = accessToken ? this.baseUrl : `${this.baseUrl}guest/`;
            
            const response = await fetch(url, {
                method: 'GET',
                headers: this.getAuthHeaders()
            });

            console.log('Checkout cart API response status:', response.status);

            if (response.ok) {
                const cartData = await response.json();
                console.log('Checkout cart data received:', cartData);
                this.cartItems = cartData.items || [];
                this.renderCheckoutCart();
            } else if (response.status === 401) {
                console.log('Unauthorized - redirecting to login');
                window.location.href = '/login/';
            } else if (response.status === 404) {
                console.log('Cart not found - showing empty cart');
                this.cartItems = [];
                this.renderCheckoutCart();
            } else {
                const errorText = await response.text();
                console.error('Failed to load cart for checkout:', response.status, errorText);
                this.showMessage('Failed to load cart items', 'error');
            }
        } catch (error) {
            console.error('Error loading cart for checkout:', error);
            this.showMessage('Error loading cart items', 'error');
        }
    }

    renderCheckoutCart() {
        const tbody = document.getElementById('checkout-cart-items');
        const whatsappBtn = document.getElementById('whatsapp-order-btn');

        if (!tbody) {
            console.error('Checkout cart items container not found');
            return;
        }

        if (this.cartItems.length === 0) {
            tbody.innerHTML = `
                <tr>
                    <td colspan="5" class="text-center py-5">
                        <img src="/static/img/vegetable-item-5.jpg" class="img-fluid mb-3" style="width: 100px; height: 100px; opacity: 0.5;" alt="Empty Cart">
                        <h5>Your cart is empty</h5>
                        <p class="text-muted">Add some products to your cart to proceed with checkout!</p>
                        <a href="/shop/" class="btn btn-primary">Continue Shopping</a>
                    </td>
                </tr>
            `;
            
            // Disable WhatsApp button if cart is empty
            if (whatsappBtn) {
                whatsappBtn.classList.add('disabled');
                whatsappBtn.disabled = true;
                whatsappBtn.textContent = 'Cart is Empty';
            }
            return;
        }

        // Render cart items
        const cartItemsHtml = this.cartItems.map(item => this.renderCheckoutItem(item)).join('');
        
        // Calculate totals
        const subtotal = this.calculateSubtotal();
        const shipping = 0; // Free shipping or calculate based on your logic
        const total = subtotal + shipping;

        // Add subtotal and total rows
        const totalsHtml = `
            <tr>
                <th scope="row"></th>
                <td class="py-5"></td>
                <td class="py-5"></td>
                <td class="py-5">
                    <p class="mb-0 text-dark py-3">Subtotal</p>
                </td>
                <td class="py-5">
                    <div class="py-3 border-bottom border-top">
                        <p class="mb-0 text-dark" id="checkout-subtotal">Rs.${subtotal.toFixed(2)}</p>
                    </div>
                </td>
            </tr>
            <tr>
                <th scope="row"></th>
                <td class="py-5">
                    <p class="mb-0 text-dark text-uppercase py-3">TOTAL</p>
                </td>
                <td class="py-5"></td>
                <td class="py-5"></td>
                <td class="py-5">
                    <div class="py-3 border-bottom border-top">
                        <p class="mb-0 text-dark" id="checkout-total">Rs.${total.toFixed(2)}</p>
                    </div>
                </td>
            </tr>
        `;

        tbody.innerHTML = cartItemsHtml + totalsHtml;

        // Enable WhatsApp button
        if (whatsappBtn) {
            whatsappBtn.classList.remove('disabled');
            whatsappBtn.disabled = false;
            whatsappBtn.textContent = 'Place Order on WhatsApp';
        }
    }

    renderCheckoutItem(item) {
        const imageUrl = item.product.image ? item.product.image : '/static/img/vegetable-item-5.jpg';
        const itemTotal = (parseFloat(item.product.price) * item.quantity).toFixed(2);
        
        return `
            <tr>
                <th scope="row">
                    <div class="d-flex align-items-center mt-2">
                        <img src="${imageUrl}" class="img-fluid rounded-circle" style="width: 90px; height: 90px;" alt="${item.product.name}" onerror="this.src='/static/img/vegetable-item-5.jpg'">
                    </div>
                </th>
                <td class="py-5">${item.product.name}</td>
                <td class="py-5">Rs.${item.product.price}</td>
                <td class="py-5">${item.quantity}</td>
                <td class="py-5">Rs.${itemTotal}</td>
            </tr>
        `;
    }

    calculateSubtotal() {
        return this.cartItems.reduce((total, item) => {
            return total + (parseFloat(item.product.price) * item.quantity);
        }, 0);
    }

    getShippingDetails() {
        const form = document.getElementById('checkout-form');
        if (!form) return null;

        const formData = new FormData(form);
        return {
            firstName: formData.get('first_name') || '',
            lastName: formData.get('last_name') || '',
            address: formData.get('address') || '',
            city: formData.get('city') || '',
            country: formData.get('country') || '',
            zipcode: formData.get('zipcode') || '',
            mobile: formData.get('mobile') || '',
            email: formData.get('email') || '',
            orderNotes: formData.get('order_notes') || ''
        };
    }

    validateForm() {
        const form = document.getElementById('checkout-form');
        if (!form) return false;

        // Remove previous validation classes
        form.classList.remove('was-validated');
        
        // Add validation class to trigger Bootstrap validation
        form.classList.add('was-validated');
        
        // Check if form is valid
        return form.checkValidity();
    }

    formatOrderDetailsForWhatsApp(orderData = null) {
        if (this.cartItems.length === 0) {
            return "Hello, I want to confirm my order.";
        }

        const shippingDetails = this.getShippingDetails();
        const subtotal = this.calculateSubtotal();
        const total = subtotal; // Add shipping if needed

        let orderText = "Hello, I want to confirm my order:\n\n";
        
        // Add order number if available
        if (orderData && orderData.order_number) {
            orderText += `📦 *ORDER NUMBER: ${orderData.order_number}*\n\n`;
        }
        
        // Add shipping details
        if (shippingDetails) {
            orderText += "📋 *SHIPPING DETAILS:*\n";
            orderText += `👤 Name: ${shippingDetails.firstName} ${shippingDetails.lastName}\n`;
            orderText += `📱 Mobile: ${shippingDetails.mobile}\n`;
            orderText += `📍 Address: ${shippingDetails.address}\n`;
            orderText += `🏙️ City: ${shippingDetails.city}\n`;
            orderText += `🌍 Country: ${shippingDetails.country}\n`;
            
            if (shippingDetails.zipcode) {
                orderText += `📮 Zipcode: ${shippingDetails.zipcode}\n`;
            }
            
            if (shippingDetails.email) {
                orderText += `📧 Email: ${shippingDetails.email}\n`;
            }
            
            if (shippingDetails.orderNotes) {
                orderText += `📝 Order Notes: ${shippingDetails.orderNotes}\n`;
            }
            
            orderText += "\n";
        }
        
        // Add cart items
        orderText += "🛒 *ORDER ITEMS:*\n";
        this.cartItems.forEach(item => {
            const itemTotal = (parseFloat(item.product.price) * item.quantity).toFixed(2);
            orderText += `• ${item.product.name} - Qty: ${item.quantity} - Rs.${itemTotal}\n`;
        });
        
        orderText += `\n💰 Subtotal: Rs.${subtotal.toFixed(2)}`;
        orderText += `\n💳 Total: Rs.${total.toFixed(2)}`;
        
        // Add order number at the end for easy reference
        if (orderData && orderData.order_number) {
            orderText += `\n\n📦 Order Reference: ${orderData.order_number}`;
        }
        
        orderText += "\n\nPlease confirm my order and provide payment details.";
        
        return orderText;
    }

    setupEventListeners() {
        const whatsappBtn = document.getElementById('whatsapp-order-btn');
        if (whatsappBtn) {
            whatsappBtn.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleWhatsAppOrder();
            });
        }

        // Add form validation on input
        const form = document.getElementById('checkout-form');
        if (form) {
            const inputs = form.querySelectorAll('input[required], textarea[required]');
            inputs.forEach(input => {
                input.addEventListener('blur', () => {
                    this.validateField(input);
                });
            });
        }

        console.log('Checkout event listeners setup complete');
    }

    validateField(field) {
        if (field.hasAttribute('required') && !field.value.trim()) {
            field.classList.add('is-invalid');
            field.classList.remove('is-valid');
        } else if (field.type === 'email' && field.value && !this.isValidEmail(field.value)) {
            field.classList.add('is-invalid');
            field.classList.remove('is-valid');
        } else {
            field.classList.add('is-valid');
            field.classList.remove('is-invalid');
        }
    }

    isValidEmail(email) {
        const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
        return emailRegex.test(email);
    }

    async handleWhatsAppOrder() {
        // Validate form first
        if (!this.validateForm()) {
            this.showMessage('Please fill in all required fields correctly.', 'error');
            return;
        }

        // Check if cart is empty
        if (this.cartItems.length === 0) {
            this.showMessage('Your cart is empty. Please add items before placing an order.', 'error');
            return;
        }

        // Check if user is authenticated
        const accessToken = localStorage.getItem('access');
        const guestToken = localStorage.getItem('guest_token');
        
        if (!accessToken && guestToken) {
            // Handle guest checkout - create user account from email
            await this.handleGuestCheckout();
        }

        // Show loading state
        const whatsappBtn = document.getElementById('whatsapp-order-btn');
        const originalText = whatsappBtn.innerHTML;
        whatsappBtn.disabled = true;
        whatsappBtn.innerHTML = '<i class="fas fa-spinner fa-spin me-2"></i>Saving Order...';

        try {
            // Save order to database first
            const orderData = await this.createOrder();
            
            if (!orderData) {
                // Error already shown in createOrder
                whatsappBtn.innerHTML = originalText;
                whatsappBtn.disabled = false;
                return;
            }

            // Order saved successfully, now open WhatsApp
            whatsappBtn.innerHTML = '<i class="fab fa-whatsapp me-2"></i>Opening WhatsApp...';
            
            const orderDetails = this.formatOrderDetailsForWhatsApp(orderData);
            const whatsappUrl = `https://wa.me/923147864467?text=${encodeURIComponent(orderDetails)}`;
            
            // Open WhatsApp in new tab
            window.open(whatsappUrl, '_blank');
            
            // Show success message
            this.showMessage(`Order #${orderData.order_number} created successfully! Opening WhatsApp...`, 'success');
            
            // Restore button after a delay
            setTimeout(() => {
                whatsappBtn.innerHTML = originalText;
                whatsappBtn.disabled = false;
            }, 2000);

        } catch (error) {
            console.error('Error in handleWhatsAppOrder:', error);
            this.showMessage('Failed to create order. Please try again.', 'error');
            whatsappBtn.innerHTML = originalText;
            whatsappBtn.disabled = false;
        }
    }

    async createOrder() {
        try {
            const shippingDetails = this.getShippingDetails();
            
            // Prepare order items from cart
            const items = this.cartItems.map(item => ({
                product_id: item.product.id,
                quantity: item.quantity
            }));

            // Get shipping address checkbox
            const shipToDifferentAddress = document.getElementById('Address-1')?.checked || false;

            // Prepare order data
            const orderData = {
                first_name: shippingDetails.firstName,
                last_name: shippingDetails.lastName,
                email: shippingDetails.email || '',
                mobile: shippingDetails.mobile,
                address: shippingDetails.address,
                city: shippingDetails.city,
                country: shippingDetails.country || 'Pakistan',
                zipcode: shippingDetails.zipcode || '',
                ship_to_different_address: shipToDifferentAddress,
                shipping_address: shipToDifferentAddress ? shippingDetails.address : '',
                shipping_city: shipToDifferentAddress ? shippingDetails.city : '',
                shipping_country: shipToDifferentAddress ? (shippingDetails.country || 'Pakistan') : '',
                shipping_zipcode: shipToDifferentAddress ? (shippingDetails.zipcode || '') : '',
                order_notes: shippingDetails.orderNotes || '',
                payment_method: 'whatsapp',
                items: items
            };

            // Call the order creation API
            const response = await fetch('/api/orders/create/', {
                method: 'POST',
                headers: this.getAuthHeaders(),
                body: JSON.stringify(orderData)
            });

            const data = await response.json();

            if (response.ok && data.order) {
                console.log('Order created successfully:', data.order);
                return data.order;
            } else {
                // Handle validation errors
                if (data.errors) {
                    const errorMessages = Object.values(data.errors).flat().join(', ');
                    this.showMessage(`Validation error: ${errorMessages}`, 'error');
                } else if (data.error) {
                    this.showMessage(data.error, 'error');
                } else {
                    this.showMessage('Failed to create order. Please try again.', 'error');
                }
                return null;
            }

        } catch (error) {
            console.error('Error creating order:', error);
            this.showMessage('Network error. Please check your connection and try again.', 'error');
            return null;
        }
    }

    async handleGuestCheckout() {
        try {
            const shippingDetails = this.getShippingDetails();
            if (!shippingDetails.email) {
                this.showMessage('Email is required for checkout.', 'error');
                return;
            }

            const guestToken = localStorage.getItem('guest_token');
            if (!guestToken) {
                this.showMessage('Guest session not found. Please try again.', 'error');
                return;
            }

            // Show loading state
            const whatsappBtn = document.getElementById('whatsapp-order-btn');
            const originalText = whatsappBtn.textContent;
            whatsappBtn.textContent = 'Creating Account...';
            whatsappBtn.disabled = true;

            // Create user account from email
            const response = await fetch('/api/auth/create-user-from-email/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCSRFToken()
                },
                body: JSON.stringify({
                    email: shippingDetails.email,
                    phone: shippingDetails.mobile,
                    first_name: shippingDetails.firstName,
                    last_name: shippingDetails.lastName,
                    guest_token: guestToken
                })
            });

            const data = await response.json();

            if (response.ok) {
                // Store tokens
                localStorage.setItem('access', data.access);
                localStorage.setItem('refresh', data.refresh);
                
                // Remove guest token
                localStorage.removeItem('guest_token');
                
                this.showMessage(data.message || 'Account created successfully!', 'success');
            } else {
                this.showMessage(data.error || 'Failed to create account', 'error');
            }

            // Restore button state
            whatsappBtn.textContent = originalText;
            whatsappBtn.disabled = false;

        } catch (error) {
            console.error('Error in guest checkout:', error);
            this.showMessage('Failed to process checkout. Please try again.', 'error');
            
            // Restore button state
            const whatsappBtn = document.getElementById('whatsapp-order-btn');
            whatsappBtn.textContent = 'Place Order on WhatsApp';
            whatsappBtn.disabled = false;
        }
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

// Initialize checkout when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    // Only initialize checkout if we're on the checkout page
    const checkoutCartItems = document.getElementById('checkout-cart-items');
    if (checkoutCartItems) {
        window.checkoutManager = new CheckoutManager();
    }
}); 