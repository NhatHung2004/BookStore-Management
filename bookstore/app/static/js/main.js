function addToCart(id, name, author, category, image, price) {
    fetch("/api/add/carts", {
        method: "POST",
        body: JSON.stringify({
            "id": id,
            "name": name,
            "author": author,
            "category": category,
            "image": image,
            "price": price
        }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then(res => res.json()).then(data => {
        let items = document.getElementsByClassName("cart-counter");
        for (let item of items)
            item.innerText = data.total_quantity;
    });
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
        for (let item of items)
            item.innerText = data.total_quantity;
    });
}
