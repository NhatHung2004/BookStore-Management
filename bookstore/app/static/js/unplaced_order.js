let cart = [];

// Hàm thêm sản phẩm vào giỏ hàng
function addToCart(productName, productPrice, productImage) {
    const existingProduct = cart.find(item => item.name === productName && item.image === productImage);

    if (existingProduct) {
        existingProduct.quantity++;
    } else {
        cart.push({ name: productName, price: productPrice, image: productImage, quantity: 1 });
    }

    updateCartDisplay();
}

// Hàm rút gọn tên sách nếu dài hơn 16 ký tự
function truncateName(name) {
    if (name.length > 16) {
        return name.slice(0, 16) + '...';
    }
    return name;
}

// Hàm cập nhật giỏ hàng
function updateCartDisplay() {
    const cartItemsContainer = document.getElementById('cartItems');
    const emptyCartMessage = document.getElementById('emptyCartMessage');
    const cartItemsContainerWrapper = document.getElementById('cartItemsContainer');

    cartItemsContainer.innerHTML = "";

    if (cart.length === 0) {
        emptyCartMessage.classList.remove('d-none');
        cartItemsContainerWrapper.classList.add('d-none');
    } else {
        emptyCartMessage.classList.add('d-none');
        cartItemsContainerWrapper.classList.remove('d-none');

        let totalAmount = 0;

        cart.forEach(item => {
    const row = document.createElement('tr');
    row.innerHTML = `
        <td><img src="${item.image}" class="product-image" alt="${item.name}" style="width: 50px; height: auto;"></td>
        <td class="product-name">${truncateName(item.name)}</td>
        <td>
            <input type="number" class="form-control quantity-input" value="${item.quantity}" min="1" onchange="updateQuantity('${item.name}', '${item.image}', this.value)">
        </td>
        <td>$${(item.price * item.quantity).toFixed(2)}</td>
    `;
    cartItemsContainer.appendChild(row);
});

        document.getElementById('totalAmount').innerText = `$${totalAmount.toFixed(2)}`;
    }
}

// Hàm cập nhật số lượng sản phẩm
function updateQuantity(productName, productImage, quantity) {
    const product = cart.find(item => item.name === productName && item.image === productImage);
    if (product) {
        product.quantity = parseInt(quantity, 10);
        updateCartDisplay();
    }
}

// Hàm thanh toán
function proceedToPayment() {
    alert("Proceeding to payment...");
}

// Hàm xóa giỏ hàng
function clearCart() {
    cart = [];
    updateCartDisplay();
}


