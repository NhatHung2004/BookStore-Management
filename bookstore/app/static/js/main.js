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

function orderOnline(customerID, cart) {
    fetch("/api/checkout", {
        method: "POST",
        body: JSON.stringify({
            "customerID": customerID,
            "cart": cart
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        var orderModal = new bootstrap.Modal(document.getElementById('orderModal'));
        orderModal.show();

        let items = document.getElementsByClassName("cart-counter");
        for (let item of items)
            item.innerText = data.stats.total_quantity;
    });

}
