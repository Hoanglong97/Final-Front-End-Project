window.onscroll = (function () { myFunction() });
var navbar = document.getElementsByClassName("header-3")[0];
var sticky = navbar.offsetTop;
var slogan = document.getElementsByClassName("slogan")[0]
function myFunction() {
    if (window.pageYOffset >= sticky) {
        navbar.classList.add("sticky")
        slogan.classList.add("slogan")
    } else {
        navbar.classList.remove("sticky");
        slogan.classList.remove("slogan")
    }
}
const showMenu = () => {
    const menu = document.getElementById('menu-bar')
    const nav = document.getElementsByClassName('navbar')[0]
    if (nav.classList.contains('hide')) {
        nav.classList.remove('hide')
        nav.classList.add('show')
    }
    else {
        nav.classList.remove('show')
        nav.classList.add('hide')
    }
}
const returnIndex = () => {
    const loader = document.getElementsByClassName("load")[0]
    setTimeout(() => {
        location.replace('./index.html')
    }, 500)
    loader.style.display = "block"
}
const returnDetail = () => {
    const loader = document.getElementsByClassName("load")[0]
    setTimeout(() => {
        location.replace('./detail.html')
    }, 500)
    loader.style.display = "block"
}
const openCart = () => {
    const loader = document.getElementsByClassName("load")[0]
    setTimeout(() => {
        location.replace('./cart.html')
    }, 500)
    loader.style.display = "block"
}
const returnLogin = () => {
    const loader = document.getElementsByClassName("load")[0]
    setTimeout(() => {
        location.replace('./login.html')
    }, 500)
    loader.style.display = "block"
}
const product = [
    {
        id: 1,
        img: "./img/1.jpg",
        name: "Acer Nitro 5",
        price: 1000,
        discount: 10,
        total: 100,
    },
    {
        id: 2,
        img: "./img/2.jpg",
        name: "Acer Nitro 5",
        price: 2000,
        discount: 10,
        total: 100,
    },
    {
        id: 3,
        img: "./img/3.jpg",
        name: "Laptop Asus",
        price: 3000,
        discount: 10,
        total: 100,
    },
    {
        id: 4,
        img: "./img/4.jpg",
        name: "PC Gaming",
        price: 4000,
        discount: 10,
        total: 100,
    },
    {
        id: 5,
        img: "./img/5.jpg",
        name: "MSI",
        price: 5000,
        discount: 10,
        total: 100,
    },
    {
        id: 6,
        img: "./img/3.jpg",
        name: "Laptop Dell",
        price: 6000,
        discount: 10,
        total: 100,
    },
    {
        id: 7,
        img: "./img/4.jpg",
        name: "Laptop Acer",
        price: 7000,
        discount: 10,
        total: 100,
    }
]
const listProduct = (items) => {
    let storage = JSON.parse(localStorage.getItem("products"))
    var total = 0
    if (storage) {
        for (let i of storage) {
            total += i.quantity
        }
    }
    document.getElementById("cartQT").innerHTML = total
    const listProduct = document.getElementById("list-product")
    for (let i of items) {
        const newItem = document.createElement("div")
        newItem.classList = "box"
        newItem.id = i.id
        newItem.img = i.img
        newItem.name = i.name
        newItem.price = i.price
        newItem.discount = i.discount
        let p = newItem.price - newItem.price * newItem.discount / 100
        newItem.innerHTML = `
        <span class="discount">${newItem.discount}%</span>
        <img src=${newItem.img} alt="" onclick="returnDetail()">
        <h3>${newItem.name}</h3>
        <div class="quantity">
            <span>Quantity: </span>
            <input id = "qt${newItem.id}" type="number" min="1" max="100" value="1">
        </div>
        <div class="price">$${p} <span>$${newItem.price}</span></div>
        <button onclick ="addCart(${newItem.id})" class="btn">Add to cart</button>
    </div>`
        listProduct.appendChild(newItem)
    }

}
