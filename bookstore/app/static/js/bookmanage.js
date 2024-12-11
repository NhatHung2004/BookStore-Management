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
