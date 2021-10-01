const addCart = (id) => {
    let storage = JSON.parse(localStorage.getItem("products"))
    for (let i of product) {
        if (i.id == id) {
            var productItem = {
                id: i.id,
                img: i.img,
                name: i.name,
                price: i.price,
                discount: i.discount,
                quantity: parseInt(document.getElementById("qt" + i.id).value)
            }
        }
    }
    var total = 0
    if (storage != null) {
        let j = true
        for (let i of storage) {
            if (i.id == productItem.id) {
                i.quantity += productItem.quantity
                j = false
            }
            total += i.quantity
        }
        if (j) {
            storage.push(productItem)
            total += productItem.quantity
        }
    }
    else {
        storage = []
        storage.push(productItem)
        total += productItem.quantity
    }
    document.getElementById("cartQT").innerHTML = total
    localStorage.setItem('products', JSON.stringify(storage))
}
const cartQT = () =>{
    let storage = JSON.parse(localStorage.getItem("products"))
    var total = 0
    for (let i of storage){
        total += i.quantity
    }
    document.getElementById("cartQT").innerHTML = total
}
const loadCart = () => {
    const listProduct = document.getElementById("list-product")
    const storage = JSON.parse(localStorage.getItem("products"))
    const cart = document.getElementsByClassName("cartProduct")[0]
    const header = document.getElementsByClassName("container")[0]
    if (storage.length == 0) {
        const h3 = document.createElement("h3")
        h3.innerHTML = `You don't have any product in cart. <a href="./index.html">Please add product to cart!</a>`
        cart.append(h3)
        header.style.display = "none"
    }
    else {
        let tongsp = 0
        for (let i of storage) {
            const newItem = document.createElement("tr")
            let p = i.price - i.price * i.discount / 100
            newItem.id = i.id
            tongsp += p * i.quantity
            newItem.innerHTML = `<td>
        <img src="${i.img}">
        </td>
        <td>${i.name}</td>
        <td>$${p}</td>
        <td>${i.quantity}</td>
        <td>$${p*i.quantity}</td>
        <td><input type="button" value="Remove" onclick="remove(${i.id})"></td>`
            listProduct.append(newItem)
        }
        document.getElementById("tong").innerHTML = "$" + tongsp
    }
    cartQT()
}
const remove = (id) => {
    const list = document.getElementById("list-product")
    const product = document.getElementById(id)
    const cart = document.getElementsByClassName("cartProduct")[0]
    const header = document.getElementsByClassName("container")[0]
    list.removeChild(product)
    let storage = JSON.parse(localStorage.getItem("products"))
    storage = storage.filter(e => e.id != id)
    let tong = 0
    for (let i of storage) {
        let p = i.price - i.price * i.discount / 100
        tong += p * i.quantity
    }
    localStorage.setItem('products', JSON.stringify(storage))
    console.log(tong)
    document.getElementById("tong").innerHTML = "$" + tong
    if (storage.length == 0) {
        const h3 = document.createElement("h3")
        h3.innerHTML = `You don't have any product in cart. <a href="./index.html">Please add product to cart!</a>`
        cart.append(h3)
        header.style.display = "none"
    }
    cartQT()
}