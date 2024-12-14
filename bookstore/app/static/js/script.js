function displayPassword() {
    var password = document.getElementById("password");
    var displayPass = document.getElementById("display-pass");
    var hidenPass = document.getElementById("hiden-pass");

    if (password.type === "password") {
        password.type = "text";
        displayPass.style.display = "block";
        hidenPass.style.display = "none";
    } else {
        password.type = "password";
        displayPass.style.display = "none";
        hidenPass.style.display = "block";
    }
}

function displayPasswordConfirm() {
    var passConfirm = document.getElementById("confirm");
    var displayPassConfirm = document.getElementById("display-confirm");
    var hidenPassConfirm = document.getElementById("hiden-confirm");

    if (passConfirm.type === "password") {
        console.log("click if");
        passConfirm.type = "text";
        displayPassConfirm.style.display = "block";
        hidenPassConfirm.style.display = "none";
    } else {
        console.log("click else");
        passConfirm.type = "password";
        displayPassConfirm.style.display = "none";
        hidenPassConfirm.style.display = "block";
    }
}

let cart = [];
// Hàm thêm sản phẩm vào giỏ hàng
function addToOrder(productName, productPrice, productImage) {
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
    updateOrderDisplay();
}
// Hàm rút gọn tên sách nếu dài hơn 16 ký tự
function truncateName(name) {
    if (name.length > 16) {
        return name.slice(0, 16) + '...';
    }
    return name;
}
// Hàm cập nhật giỏ hàng
function updateOrderDisplay() {
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
function clearOrder() {
    cart = [];
    updateOrderDisplay();
}



// Mảng để lưu trữ dữ liệu sách
let books = [];
function showDialog(action, bookIndex = null) {
    const modalTitle = document.getElementById('modalTitle');
    const bookForm = document.getElementById('bookForm');
    if (action === 'add') {
        modalTitle.textContent = 'Thêm sách mới';
        bookForm.reset(); // Đặt lại các trường trong biểu mẫu
        bookForm.dataset.index = ""; // Xóa chỉ số
    } else if (action === 'edit') {
        modalTitle.textContent = 'Chỉnh sửa sách';
        const book = books[bookIndex];
        bookForm.dataset.index = bookIndex; // Lưu chỉ số để chỉnh sửa
        // Điền thông tin hiện tại vào các trường biểu mẫu
        document.getElementById('bookName').value = book.name;
        document.getElementById('bookPrice').value = book.price;
        document.getElementById('bookAuthor').value = book.author;
        document.getElementById('bookStock').value = book.stock;
        document.getElementById('bookDate').value = book.date;
        document.getElementById('bookCategory').value = book.category;
    }
    const modal = new bootstrap.Modal(document.getElementById('bookModal'));
    modal.show();
}
function saveBook() {
    const bookName = document.getElementById('bookName').value;
    const bookPrice = document.getElementById('bookPrice').value;
    const bookAuthor = document.getElementById('bookAuthor').value;
    const bookStock = document.getElementById('bookStock').value;
    const bookDate = document.getElementById('bookDate').value;
    const bookImage = document.getElementById('bookImage').files[0];
    const bookCategory = document.getElementById('bookCategory').value;
    if (!bookName || !bookPrice || !bookAuthor || !bookCategory) {
        alert('Vui lòng điền đầy đủ các trường bắt buộc.');
        return;
    }
    // Chuẩn bị dữ liệu sách
    const bookData = {
        name: bookName,
        price: bookPrice,
        author: bookAuthor,
        stock: bookStock,
        date: bookDate,
        category: bookCategory,
        image: bookImage ? bookImage.name : "Không có hình ảnh",
    };
    // Kiểm tra đang chỉnh sửa hay thêm mới
    const bookForm = document.getElementById('bookForm');
    const bookIndex = bookForm.dataset.index;
    if (bookIndex === "") {
        // Thêm sách mới
        books.push(bookData);
    } else {
        // Chỉnh sửa sách hiện tại
        books[bookIndex] = bookData;
    }
    updateBookTable();
    alert('Lưu sách thành công!');
    const modal = bootstrap.Modal.getInstance(document.getElementById('bookModal'));
    modal.hide();
}
function updateBookTable() {
    const tableBody = document.getElementById('bookTableBody');
    tableBody.innerHTML = ""; // Xóa các dòng hiện tại
    books.forEach((book, index) => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td>${index + 1}</td>
            <td>${book.name}</td>
            <td><img src="${book.image}" alt="Hình ảnh sách" width="50"></td>
            <td>${book.category}</td>
            <td>$${book.price}</td>
            <td>${book.author}</td>
            <td>${book.stock}</td>
            <td>${book.date}</td>
            <td>
                <button class="btn-icon edit" onclick="showDialog('edit', ${index})" title="Chỉnh sửa">
                    <i class="fas fa-pencil-alt"></i>
                </button>
                <button class="btn-icon delete" onclick="deleteBook(${index})" title="Xóa">
                    <i class="fas fa-trash"></i>
                </button>
            </td>
        `;
        tableBody.appendChild(row);
    });
}
function deleteBook(index) {
    if (confirm("Bạn có chắc chắn muốn xóa sách này?")) {
        books.splice(index, 1);
        updateBookTable();
    }
}


document.addEventListener('DOMContentLoaded', function () {
    const paymentMethodRadios = document.querySelectorAll('input[name="paymentMethod"]');
    const addressInput = document.getElementById('address');
    const addressLabel = document.querySelector('label[for="address"]');
    const checkoutButton = document.querySelector('.payment-checkout-radio-btn button');

    // Hiện hoặc ẩn ô địa chỉ và label khi thay đổi phương thức thanh toán
    paymentMethodRadios.forEach(radio => {
        radio.addEventListener('change', function () {
            if (radio.value === 'direct') {
                addressInput.style.display = 'block';
                addressLabel.style.display = 'block';
            } else {
                addressInput.style.display = 'none';
                addressLabel.style.display = 'none';
            }
        });
    });

    // Đặt mặc định ẩn ô địa chỉ và label nếu chọn VNPAY
    if (document.getElementById('credit').checked) {
        addressInput.style.display = 'none';
        addressLabel.style.display = 'none';
    }

});
