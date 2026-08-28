const text = document.querySelector('.circle');
        text.innerHTML = text.textContent.replace(/\S/g, "<span>$&</span>");

        const element = document.querySelectorAll('.circle span');
        for (let i = 0; i < element.length; i++) {
            element[i].style.transform = "rotate(" + i * 14.5 + "deg)"
        }
        // Initialize cart with one default item for demonstration
let cart = [
    { id: 201, name: 'Wellness Dog Shampoo', price: 18.00, img: 'product03.png', qty: 1 }
];

// Open/Close Drawer
function toggleCart() {
    document.getElementById('cartDrawer').classList.toggle('open');
    const overlay = document.querySelector('.cart-overlay');
    overlay.style.display = (overlay.style.display === 'block') ? 'none' : 'block';
}

// Add Item to Cart
function addToCart(id, name, price, img) {
    const existingItem = cart.find(item => item.id === id);
    if (existingItem) {
        existingItem.qty++;
    } else {
        cart.push({ id, name, price, img, qty: 1 });
    }
    updateCartUI();
    // Auto-open drawer when adding
    if(!document.getElementById('cartDrawer').classList.contains('open')) toggleCart();
}

// Update Quantity (+ / -)
function updateQty(id, delta) {
    const item = cart.find(i => i.id === id);
    if (item) {
        item.qty += delta;
        if (item.qty < 1) removeFromCart(id);
    }
    updateCartUI();
}

// Remove Item
function removeFromCart(id) {
    cart = cart.filter(item => item.id !== id);
    updateCartUI();
}

// Refresh UI and LocalStorage
function updateCartUI() {
    const container = document.getElementById('cart-items-container');
    const totalDisp = document.getElementById('cart-total');
    const countBadge = document.getElementById('cart-count');

    container.innerHTML = "";
    let total = 0;
    let totalQty = 0;

    if (cart.length === 0) {
        container.innerHTML = `<div class="text-center mt-5"><p class="text-muted">Your basket is empty!</p></div>`;
    } else {
        cart.forEach(item => {
            const itemTotal = item.price * item.qty;
            total += itemTotal;
            totalQty += item.qty;
            // Replace your innerHTML generation with this specific structure:
container.innerHTML += `
    <div class="cart-item">
        <!-- <img src="assets/img/product/${item.img}" onerror="this.src='assets/img/products/products_img01.jpg'"> -->
        <div class="cart-item-info">
            <span class="cart-item-name">${item.name}</span>
            <span class="cart-item-price">$${itemTotal.toFixed(2)}</span>
            <div class="qty-row">
                <div class="qty-box">
                    <button class="qty-btn" onclick="updateQty(${item.id}, -1)">-</button>
                    <div class="qty-num">${item.qty}</div>
                    <button class="qty-btn" onclick="updateQty(${item.id}, 1)">+</button>
                </div>
                <a href="javascript:void(0)" class="btn-remove" onclick="removeFromCart(${item.id})">Remove</a>
            </div>
        </div>
    </div>`;
        });
    }
    countBadge.innerText = totalQty;
    totalDisp.innerText = `$${total.toFixed(2)}`;
    // Sync with other pages via local storage
    localStorage.setItem('petCart', JSON.stringify(cart));
}

// Initial Run
window.onload = updateCartUI;

$(document).ready(function() {
    // Check if a user is logged in (Data from Customer Table)
    const loggedInUser = localStorage.getItem('cust_name'); 
    
    if (loggedInUser) {
        // Update the label with the actual name
        $('#header-user-name').text(loggedInUser);
    } else {
        // Default for guests
        $('#header-user-name').text("Vraj");
    }
});