function switchPay(type) {
        $('.pay-tab').removeClass('active');
        if(type === 'card') {
            $('.pay-tab').eq(0).addClass('active');
            $('#card-form').stop().fadeIn(400); $('#upi-form').hide();
        } else {
            $('.pay-tab').eq(1).addClass('active');
            $('#card-form').hide(); $('#upi-form').stop().fadeIn(400);
        }
    }

    // Function to show the stylish notification
    function showPetpalToast(message) {
        $('#cart-toast').text(message).fadeIn(400).delay(3000).fadeOut(400);
    }

    $(document).ready(function() {
        if (typeof SVGInject !== 'undefined') SVGInject($(".injectable"));
        if (typeof WOW !== 'undefined') new WOW().init();

        // 1. DATA SYNC & PRICE CALCULATION
        const unitPrice = 29.00;
        let savedQty = localStorage.getItem('petpal_cart_qty') || 1;

        function updateCartPrices(qty) {
            const finalPrice = (qty * unitPrice).toFixed(2);
            $('#display-qty').text(qty);
            $('#display-subtotal, #sum-subtotal, #sum-total').text('$' + finalPrice);
        }

        // Initialize UI on load
        updateCartPrices(savedQty);

        // 2. ADDRESS AUTO-LOAD
        if (localStorage.getItem('petpal_saved_address')) {
            const addr = JSON.parse(localStorage.getItem('petpal_saved_address'));
            $('#ship-name').val(addr.name);
            $('#ship-phone').val(addr.phone);
            $('#ship-street').val(addr.street);
            $('#ship-city').val(addr.city);
            $('#ship-state').val(addr.state);
            $('#ship-pin').val(addr.pin);
            $('#saveAddressToggle').prop('checked', true);
        }

        // 3. HANDLE SAVE ADDRESS & ORDER
        $('#placeOrderBtn').on('click', function(e) {
            // Check if address is filled (Simple validation)
            if($('#ship-name').val() === "") {
                e.preventDefault();
                showPetpalToast("Please provide a delivery address! 📍");
                return;
            }

            if ($('#saveAddressToggle').is(':checked')) {
                const addressData = {
                    name: $('#ship-name').val(),
                    phone: $('#ship-phone').val(),
                    street: $('#ship-street').val(),
                    city: $('#ship-city').val(),
                    state: $('#ship-state').val(),
                    pin: $('#ship-pin').val()
                };
                localStorage.setItem('petpal_saved_address', JSON.stringify(addressData));
            }
        });

        // 4. FAST TRACK LOGIC (BUY NOW)
        const urlParams = new URLSearchParams(window.location.search);
        if (urlParams.has('checkout') && urlParams.get('checkout') === 'direct') {
            showPetpalToast("Fast-Tracked to Delivery! 🐾");
            setTimeout(function() {
                $('html, body').animate({
                    scrollTop: $("#address-section").offset().top - 20
                }, 800);
                $("#address-section").css({
                    "border-color": "var(--tg-brand-color)",
                    "box-shadow": "0 0 25px rgba(137, 75, 141, 0.2)"
                });
            }, 400);
        }
    });
	function updateUniversalBadge() {
        const badge = document.getElementById('header-cart-count');
        if (!badge) return;

        // Get the saved quantity
        const savedQty = localStorage.getItem('petpal_cart_qty');

        if (savedQty && parseInt(savedQty) > 0) {
            badge.textContent = savedQty;
            badge.style.display = 'flex'; // Show the badge
        } else {
            badge.textContent = '0';
            // Optional: hide the badge if you want it to look empty
            // badge.style.display = 'none'; 
        }
    }

    $(document).ready(function() {
        // Run immediately on page load
        updateUniversalBadge();

        // Listen for changes in other tabs/pages
        window.addEventListener('storage', function(e) {
            if (e.key === 'petpal_cart_qty') {
                updateUniversalBadge();
            }
        });
    });