function addToCart(id, name, author, category, image, price, is_authenticated) {
    if (is_authenticated === 'True') {
        fetch("/api/carts", {
            method: "POST",
            body: JSON.stringify({
                "id": id,
                "name": name,
                "author": author,
                "category": category,
                "image": image,
                "price": price,
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            if (Object.keys(data).length === 0) {

            } else {
                let items = document.getElementsByClassName("cart-counter");
                for (let item of items)
                    item.innerText = data.total_quantity;
            }

        });
    } else {
        const authModal = new bootstrap.Modal(document.getElementById('authModal'));
        authModal.show();
    }
}

function addCartFromOrder() {
    if (cartOrder != []) {
        fetch("/api/cartOrders", {
            method: "POST",
            body: JSON.stringify({
                "cartOrder": cartOrder
            }),
            headers: {
                'Content-Type': 'application/json'
            }
        }).then(res => res.json()).then(data => {
            window.location.href = data.url;
        });
    };
}

function removeCartFromOrder() {
    clearOrder()
    fetch("/api/cartOrders", {
        method: "DELETE"
    }).then(res => res.json()).then(data => {
        alert("Giỏ hàng rỗng")
    })
}

function removeFromCart(id) {
    if (confirm("Bạn muốn xóa sản phẩm?") === true) {
        fetch(`/api/carts/${id}`, {
            method: "delete"
        }).then(res => res.json()).then(data => {
            let items = document.getElementsByClassName("cart-counter");
            document.getElementById(`cart${id}`).style.display = "none"
            for (let item of items)
                item.innerText = data.total_quantity;
        });
    }
}

function updateQuantity(id, btn) {
    fetch(`/api/carts/${id}`, {
        method: "PUT",
        body: JSON.stringify({
            "btn": btn
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        document.getElementById(`quantity-input-${data.id}`).value = data.quantity

        let items = document.getElementsByClassName("cart-counter");
        for (let item of items)
            item.innerText = data.total_quantity;
    });
}

function payment(amount) {
    if (amount != 0) {
        let paymentMethod = document.querySelector('input[name="paymentMethod"]:checked').value;

        if (paymentMethod === 'vnpay') {
            fetch('/api/create_payment', {
                method: "POST",
                body: JSON.stringify({
                    'amount': amount
                }),
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(res => res.json()).then(data => {
                console.log("Payment Data:", data);
                if (data.payment_url) {
                    window.location.href = data.payment_url;
                } else {
                    alert('Lỗi khi tạo thanh toán VNPay!');
                };
            })
        } else {
            fetch('/api/payment-direct', {
                method: "POST",
                headers: {
                    'Content-Type': 'application/json'
                }
            }).then(res => res.json()).then(data => {
                window.location.href = "http://127.0.0.1:5000/";
            });
        }
    }
}

// button them giam so luong trong book-detail
const decreaseBtn = document.getElementById("book-detail-decrease");
const increaseBtn = document.getElementById("book-detail-increase");
const quantityInput = document.getElementById("book-detail-quantity");

decreaseBtn.onclick = () => {
    let value = parseInt(quantityInput.value);
    if (value > 1) quantityInput.value = value - 1;
};

increaseBtn.onclick = () => {
    let value = parseInt(quantityInput.value);
    if (value < 20) quantityInput.value = value + 1;
};
