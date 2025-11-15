(function ($) {
    "use strict";

    // Spinner
    var spinner = function () {
        setTimeout(function () {
            if ($('#spinner').length > 0) {
                $('#spinner').removeClass('show');
            }
        }, 1);
    };
    spinner(0);


    // Fixed Navbar
    $(window).scroll(function () {
        if ($(window).width() < 992) {
            if ($(this).scrollTop() > 55) {
                $('.fixed-top').addClass('shadow');
            } else {
                $('.fixed-top').removeClass('shadow');
            }
        } else {
            if ($(this).scrollTop() > 55) {
                $('.fixed-top').addClass('shadow').css('top', -55);
            } else {
                $('.fixed-top').removeClass('shadow').css('top', 0);
            }
        } 
    });
    
    
   // Back to top button
   $(window).scroll(function () {
    if ($(this).scrollTop() > 300) {
        $('.back-to-top').fadeIn('slow');
    } else {
        $('.back-to-top').fadeOut('slow');
    }
    });
    $('.back-to-top').click(function () {
        $('html, body').animate({scrollTop: 0}, 100, 'easeInOutExpo');
        return false;
    });


    // Testimonial carousel
    $(".testimonial-carousel").owlCarousel({
        autoplay: true,
        autoplayTimeout: 2000,
        smartSpeed: 1000,
        center: false,
        dots: true,
        loop: true,
        margin: 25,
        nav : true,
        navText : [
            '<i class="bi bi-arrow-left"></i>',
            '<i class="bi bi-arrow-right"></i>'
        ],
        responsiveClass: true,
        responsive: {
            0:{
                items:1
            },
            576:{
                items:1
            },
            768:{
                items:1
            },
            992:{
                items:2
            },
            1200:{
                items:2
            }
        }
    });


    // vegetable carousel
    $(function() {
        const totalProducts = $(".vegetable-carousel .vesitable-item").length;
    
        $(".vegetable-carousel").owlCarousel({
            autoplay: true,
            smartSpeed: 1500,
            center: false,
            dots: true,
            loop: totalProducts >= 4,  
            margin: 25,
            nav: true,
            navText: [
                '<i class="bi bi-arrow-left"></i>',
                '<i class="bi bi-arrow-right"></i>'
            ],
            responsiveClass: true,
            responsive: {
                0: {
                    items: 1
                },
                576: {
                    items: 1
                },
                768: {
                    items: 2
                },
                992: {
                    items: 3
                },
                1200: {
                    items: 4
                }
            }
        });
    });
    


    // Modal Video
    $(document).ready(function () {
        var $videoSrc;
        $('.btn-play').click(function () {
            $videoSrc = $(this).data("src");
        });
        console.log($videoSrc);

        $('#videoModal').on('shown.bs.modal', function (e) {
            $("#video").attr('src', $videoSrc + "?autoplay=1&amp;modestbranding=1&amp;showinfo=0");
        })

        $('#videoModal').on('hide.bs.modal', function (e) {
            $("#video").attr('src', $videoSrc);
        })
    });



    // Product Quantity
    $('.quantity button').on('click', function () {
        var button = $(this);
        var oldValue = button.parent().parent().find('input').val();
        if (button.hasClass('btn-plus')) {
            var newVal = parseFloat(oldValue) + 1;
        } else {
            if (oldValue > 0) {
                var newVal = parseFloat(oldValue) - 1;
            } else {
                newVal = 0;
            }
        }
        button.parent().parent().find('input').val(newVal);
    });

    // Featured Products Vertical Slideshow
    $(function() {
        const $container = $('.featured-products-container');
        const $wrapper = $('.featured-products-wrapper');
        const $items = $('.featured-product-item');
        
        if ($container.length && $items.length > 3) {
            const itemHeight = 133; // Height of each item in pixels
            const visibleItems = 3;
            const totalItems = $items.length;
            const maxScroll = (totalItems - visibleItems) * itemHeight;
            let currentPosition = 0;
            
            // Auto-scroll functionality
            let autoScrollInterval;
            
            function startAutoScroll() {
                autoScrollInterval = setInterval(function() {
                    if (currentPosition >= maxScroll) {
                        currentPosition = 0;
                    } else {
                        currentPosition += itemHeight;
                    }
                    $wrapper.css('transform', `translateY(-${currentPosition}px)`);
                }, 2000); // Auto-scroll every 2 seconds
            }
            
            function stopAutoScroll() {
                clearInterval(autoScrollInterval);
            }
            
            // Start auto-scroll on page load
            startAutoScroll();
            
            // Pause auto-scroll on hover
            $container.hover(
                function() { stopAutoScroll(); },
                function() { startAutoScroll(); }
            );
        }
    });

})(jQuery);

// Function to handle "Add to Cart" button click on index.html
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

   // Function to handle "View Details" button click on index.html
   function handleViewDetails(event, productId) {
    event.preventDefault();
    console.log('handleViewDetails called with productId:', productId);
    window.location.href = `/product-detail/${productId}/`;
  }
  
  // Helper function to get CSRF token
  function getCSRFToken() {
    const token = document.querySelector('[name=csrfmiddlewaretoken]');
    return token ? token.value : '';
  }

  // Function to update cart badge in navbar
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

// Clothing Filter Functionality
$(document).ready(function() {
    // Handle clothing season filter
    $('input[name="clothingSeason"]').on('change', function() {
        filterClothingProducts();
    });
    
    // Handle clothing gender filter
    $('input[name="clothingGender"]').on('change', function() {
        filterClothingProducts();
    });
});

function filterClothingProducts() {
    const season = $('input[name="clothingSeason"]:checked').val();
    const gender = $('input[name="clothingGender"]:checked').val();
    const container = $('#clothingProductsContainer');
    
    // Show loading state
    container.html('<div class="col-12 text-center"><div class="spinner-border text-primary" role="status"><span class="visually-hidden">Loading...</span></div></div>');
    
    // Build API URL
    let apiUrl = '/api/products/filter/?product_type=clothing';
    
    if (season && season !== 'all') {
        apiUrl += `&season=${season}`;
    }
    
    if (gender && gender !== 'all') {
        apiUrl += `&gender=${gender}`;
    }
    
    // Fetch filtered products
    fetch(apiUrl)
        .then(response => response.json())
        .then(data => {
            if (data.results && data.results.length > 0) {
                renderClothingProducts(data.results);
            } else {
                container.html('<div class="col-12 text-center"><p class="text-muted">No products found with the selected filters.</p></div>');
            }
        })
        .catch(error => {
            console.error('Error fetching filtered products:', error);
            container.html('<div class="col-12 text-center"><p class="text-danger">Error loading products. Please try again.</p></div>');
        });
}

function renderClothingProducts(products) {
    const container = $('#clothingProductsContainer');
    container.empty();
    
    products.forEach(product => {
        const productHtml = `
            <div class="col-md-6 col-lg-4 col-xl-3 mt-4 d-flex">
                <div class="rounded position-relative fruite-item w-100 d-flex flex-column">
                    <div class="fruite-img">
                        <img loading="lazy" width="300" height="200" src="${product.image || '/static/images/no-image.jpg'}" class="img-fluid w-100 rounded-top" alt="${product.name}">
                    </div>
                    <div class="text-white bg-secondary px-3 py-1 rounded position-absolute" style="top: 10px; left: 10px;">${product.product_type}</div>
                    <div class="p-4 border border-secondary border-top-0 rounded-bottom d-flex flex-column flex-grow-1">
                        <h4>${product.name}</h4>
                        <p class="flex-grow-1">${product.description || ''}</p>
                        <p class="text-dark fs-5 fw-bold me-2 pt-2">RS ${product.price}</p>
                        <button onclick="handleViewDetails(event, '${product.id}')" class="btn border border-secondary rounded-pill text-primary mb-3" style="padding: 8px 16px;">
                            <i class="fa fa-eye me-2 text-primary"></i> View Details
                        </button>
                        <button onclick="handleAddToCart(event, '${product.id}')" class="btn border border-secondary rounded-pill text-primary" style="padding: 8px 16px;">
                            <i class="fa fa-shopping-bag me-2 text-primary"></i> Add to cart
                        </button>
                    </div>
                </div>
            </div>
        `;
        container.append(productHtml);
    });
}