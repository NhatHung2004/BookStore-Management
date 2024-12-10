function addToCart(id, name, author, category, image, price, is_authenticated) {
    if (is_authenticated === 'True') {
        fetch("/api/add/carts", {
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

function removeFromCart(id) {
    fetch("/api/remove/carts", {
        method: "POST",
        body: JSON.stringify({
            "id": id
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let items = document.getElementsByClassName("cart-counter");
        let i = a.parentElement;
        i.remove()
        for (let item of items)
            item.innerText = data.total_quantity;
    });
}

function updateQuantity(id) {
    fetch("/api/updateQuantity/carts", {
        method: "POST",
        body: JSON.stringify({
            "id": id
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
    var orderID = document.getElementById("orderID").value
    fetch('/create_payment', {
        method: "POST",
        body: JSON.stringify({
            'order_id': orderID, // Mã đơn hàng
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
        }
    })
}

function orderOnline(customerID, phone, cart) {
    fetch("/api/checkout", {
        method: "POST",
        body: JSON.stringify({
            "customerID": customerID,
            "phone": phone,
            "cart": cart,
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(async data => {
        var orderModal = new bootstrap.Modal(document.getElementById('orderModal'));
        orderModal.show();

        document.getElementById("orderID").value = data.orderID
        document.getElementById("total_amount").value = data.stats.total_amount

        // let items = document.getElementsByClassName("cart-counter");
        // for (let item of items)
        //     item.innerText = data.stats.total_quantity;
    });

}
