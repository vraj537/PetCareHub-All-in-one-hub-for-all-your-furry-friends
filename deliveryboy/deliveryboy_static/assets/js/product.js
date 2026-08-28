$(document).on('click', '.add-to-cart-btn', function(e) {
    e.preventDefault();

    // 1. Extract data from the clicked button
    const product = {
        id: $(this).data('id'),
        name: $(this).data('name'),
        price: Number($(this).data('price')),
        image: $(this).data('image'),
        qty: 1
    };

    // 2. Get current cart from localStorage
    let cart = JSON.parse(localStorage.getItem('pet_cart')) || [];

    // 3. Check if item exists to update quantity
    const existingItem = cart.find(item => item.id === product.id);

    if (existingItem) {
        existingItem.qty = Number(existingItem.qty) + 1;
    } else {
        cart.push(product);
    }

    // 4. Save and Update Header
    localStorage.setItem('pet_cart', JSON.stringify(cart));
    
    // Call the sync function in your header1.html
    if (typeof syncHeaderBadge === "function") {
        syncHeaderBadge();
    }

    alert("🐾 " + product.name + " added to your basket!");
});