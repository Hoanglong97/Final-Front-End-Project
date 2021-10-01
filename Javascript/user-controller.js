const popup = () => {
    let modalBtn = document.getElementById("popup-btn");
    let signIn = document.querySelector(".signIn");
    let modal = document.querySelector(".popup");
    let closeBtn = document.querySelector(".close-btn");
    // let name = document.getElementById("name")
    // let pass = document.getElementById("pass")
    modalBtn.onclick = function () {
        modal.style.display = "block"
        signIn.style.display = "none"
        // name.removeAttribute('required')
        // pass.removeAttribute('required')
    }
    closeBtn.onclick = function () {
        modal.style.display = "none"
        signIn.style.display = "block"
    }
}
const loginIndex = () => {
    let name = document.getElementById("name").value
    let pass = document.getElementById("pass").value
    $.ajax({
        url: "http://127.0.0.1:8000/v1/users/login",
        data: '{"username": "' + name + '", "password" : "' + pass + '"}',
        method: "POST",
        success: data => {
            if (data) {
                const loader = document.getElementsByClassName("load")[0]
                setTimeout(() => {
                    location.replace('./index.html')
                }, 2000)
                loader.style.display = "block"
            }
            else {
                window.alert("Vui lòng nhập lại !")
            }
        },
        error: (xhr, textStatus, errorThrown) => {
            console.log(textStatus);
        }
    })
}
const SignUp = () => {
    let name = document.getElementById("username").value
    let pass = document.getElementById("password").value
    $.ajax({
        url: "http://127.0.0.1:8000/v1/users/",
        data: '{"username": "' + name + '", "password" : "' + pass + '"}',
        method: "POST",
        success: data => {
            window.alert("Đăng ký thành công")
            location.replace("./login.html")
        },
        error: (xhr, textStatus, errorThrown) => {
            window.alert("Đăng ký thẩt bại")
        }
    })
}