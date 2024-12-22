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
        location.reload();
        console.log(data);
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

function updateQuantityCartOrder(id, obj) {
    fetch(`/api/cartOrders/${id}`, {
        method: "put",
        body: JSON.stringify({
            quantity: obj.value
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(data => {
        console.log(data);
    })
}

function payOrder(phone) {
    fetch("/api/orders", {
        method: "POST",
        body: JSON.stringify({
            "phone": phone
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        window.location.href = data.url;
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
                window.location.href = "http://127.0.0.1:5002/";
            });
        }
    }
}

function addComment(book_id) {
    fetch(`/api/books/${book_id}/comments`, {
        method: "post",
        body: JSON.stringify({
            'content': document.getElementById("comment").value
        }),
        headers: {
            "Content-Type": "application/json"
        }
    }).then(res => res.json()).then(c => {
        // location.reload();
        let html =  `
            <div class="book-detail-review">
                <img src="${ c.user.avatar }" alt="User Avatar" class="book-detail-avatar">
                <div class="book-detail-review-content">
                    <p class="book-detail-review-name">${ c.user.name }</p>
                    <p>${ c.content }</p>
                    <p class="book-detail-review-time">${ moment(c.created_date).locale("vi").fromNow() }</p>
                </div>
            </div>
        `;

        let h = document.getElementById("comments");
        h.innerHTML = html + h.innerHTML;
    })
}
