        let cart = [];
        // Hàm thêm sản phẩm vào giỏ hàng
        function addToCart(productName, productPrice, productImage) {
            // Kiểm tra nếu sản phẩm đã có trong giỏ hàng bằng cách so sánh tên sản phẩm và hình ảnh
            const existingProduct = cart.find(item => item.name === productName && item.image === productImage);

            if (existingProduct) {
                // Nếu sản phẩm đã có, tăng số lượng lên 1
                existingProduct.quantity++;
            } else {
                // Nếu sản phẩm chưa có, thêm mới vào giỏ hàng
                cart.push({ name: productName, price: productPrice, image: productImage, quantity: 1 });
            }

            // Cập nhật lại giao diện giỏ hàng
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

            // Xóa hết sản phẩm cũ trong giỏ hàng
            cartItemsContainer.innerHTML = "";

            if (cart.length === 0) {
                // Nếu giỏ hàng trống, hiển thị thông báo
                emptyCartMessage.classList.remove('d-none');
                cartItemsContainerWrapper.classList.add('d-none');
            } else {
                // Nếu giỏ hàng có sản phẩm, ẩn thông báo và hiển thị các sản phẩm trong giỏ hàng
                emptyCartMessage.classList.add('d-none');
                cartItemsContainerWrapper.classList.remove('d-none');

                let totalAmount = 0;

                // Lặp qua từng sản phẩm trong giỏ hàng
                cart.forEach(item => {
                    const row = document.createElement('tr');
                    row.innerHTML = `
                        <td><img src="${item.image}" class="product-image" alt="${item.name}"></td>
                        <td class="product-name">${truncateName(item.name)}</td>
                        <td>
                            <input type="number" class="form-control quantity-input" value="${item.quantity}" min="1" onchange="updateQuantity('${item.name}', '${item.image}', this.value)">
                        </td>
                        <td>$${(item.price * item.quantity).toFixed(2)}</td>
                    `;
                    cartItemsContainer.appendChild(row);

                    // Tính tổng số tiền
                    totalAmount += item.price * item.quantity;
                });

                // Cập nhật tổng giá trị đơn hàng
                document.getElementById('totalAmount').innerText = `$${totalAmount.toFixed(2)}`;
            }
        }

        // Cập nhật số lượng sản phẩm trong giỏ hàng
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