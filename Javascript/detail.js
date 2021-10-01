const loadDetail = () => {
    const listProduct = document.getElementById("list-product")
    const storage = JSON.parse(localStorage.getItem("products"))
    let tongsp = 0
    for (let i of storage) {
        const newItem = document.createElement("tr")
        let p = i.price - i.price * i.discount / 100
        newItem.id = i.id
        tongsp += p*i.quantity
        newItem.innerHTML = `<td>
        <img src="${i.img}">
        </td>
        <td>${i.name}</td>
        <td>${i.discount}%</td>
        <td>${i.quantity}</td>
        <td>$${p}</td>
        <td><input type="button" value="Remove" onclick="remove(${i.id})"></td>`
        listProduct.append(newItem)
    }
    document.getElementById("tong").innerHTML = "$" + tongsp
}