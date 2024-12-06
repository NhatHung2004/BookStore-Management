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

// document.querySelector("#search-btn").onclick = () => {
//     searchForm.classList.toggle("active");
// };

// var navLinks = document.querySelectorAll("header .navbar a");
// var section = document.querySelectorAll("section");

// window.onscroll = () => {
//     searchForm.classList.remove("active");

//     section.forEach((sec) => {
//         var top = window.scrollY;
//         var height = sec.offsetHeight;
//         var offset = sec.offsetTop - 150;
//         var id = sec.getAttribute("id");

//         if (top >= offset && top < offset + height) {
//             navLinks.forEach((links) => {
//                 links.classList.remove("active");
//                 document
//                     .querySelector("header .navbar a[href *= " + id + "]")
//                     .classList.add("active");
//             });
//         }
//     });

//     if (window.scrollY > 80) {
//         document.querySelector(".header .header-2").classList.add("active");
//     } else {
//         document.querySelector(".header .header-2").classList.remove("active");
//     }
// };
// function loader() {
//     document.querySelector(".loader-container").classList.add("active");
// }
// function fadeOut() {
//     setTimeout(loader, 4000);
// }
// window.onload = () => {
//     if (window.scrollY > 80) {
//         document.querySelector(".header .header-2").classList.add("active");
//     } else {
//         document.querySelector(".header .header-2").classList.remove("active");
//     }
//     fadeOut();
// };

// var swiper = new Swiper(".books-slider", {
//     loop: true,
//     centeredSlides: true,
//     autoplay: {
//         delay: 3000,
//         disableOnInteraction: false,
//     },
//     breakpoints: {
//         0: {
//             slidesPerView: 1,
//         },
//         768: {
//             slidesPerView: 2,
//         },
//         1024: {
//             slidesPerView: 3,
//         },
//     },
// });

// var swiper = new Swiper(".populer-slider", {
//     spaceBetween: 10,
//     loop: true,
//     centeredSlides: true,
//     autoplay: {
//         delay: 5000,
//         disableOnInteraction: false,
//     },
//     navigation: {
//         nextEl: ".swiper-button-next",
//         prevEl: ".swiper-button-prev",
//     },
//     breakpoints: {
//         0: {
//             slidesPerView: 1,
//         },
//         450: {
//             slidesPerView: 2,
//         },
//         768: {
//             slidesPerView: 3,
//         },
//         1024: {
//             slidesPerView: 4,
//         },
//     },
// });

// var swiper = new Swiper(".new-slider", {
//     spaceBetween: 10,
//     loop: true,
//     centeredSlides: true,
//     autoplay: {
//         delay: 3500,
//         disableOnInteraction: false,
//     },
//     breakpoints: {
//         0: {
//             slidesPerView: 1,
//         },
//         768: {
//             slidesPerView: 2,
//         },
//         1024: {
//             slidesPerView: 3,
//         },
//     },
// });

// var swiper = new Swiper(".new-slider-2", {
//     spaceBetween: 10,
//     loop: true,
//     centeredSlides: true,
//     autoplay: {
//         delay: 6000,
//         disableOnInteraction: false,
//     },
//     breakpoints: {
//         0: {
//             slidesPerView: 1,
//         },
//         768: {
//             slidesPerView: 2,
//         },
//         1024: {
//             slidesPerView: 3,
//         },
//     },
// });

// var swiper = new Swiper(".reviews-slider", {
//     spaceBetween: 10,
//     grabCursor: true,
//     loop: true,
//     centeredSlides: true,
//     autoplay: {
//         delay: 33500,
//         disableOnInteraction: false,
//     },
//     breakpoints: {
//         0: {
//             slidesPerView: 1,
//         },
//         768: {
//             slidesPerView: 2,
//         },
//         1024: {
//             slidesPerView: 3,
//         },
//     },
// });

// let loadMoreBtn = document.querySelector("#load-more");
// let currentItem = 3;

// loadMoreBtn.onclick = () => {
//     let boxes = [...document.querySelectorAll(".container .box-container .box")];
//     for (var i = currentItem; i < currentItem + 3; i++) {
//         boxes[i].style.display = "inline-block";
//     }
//     currentItem += 3;

//     if (currentItem >= boxes.length) {
//         loadMoreBtn.style.display = "none";
//     }
// };

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
