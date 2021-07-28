// const callAPI = () => {
//     $.ajax({
//         url: "https://60f18a5b38ecdf0017b0fcdc.mockapi.io/Product",
//         method: "GET", // GET or POST or PUT or DELETE
//         contentType: "application/x-www-form-urlencoded; charset=UTF-8",
//         success: data => {
//             const { result } = data;

//             // Hide page
//             $(".card-row").fadeOut(1000);

//             // show new item
//             for (let item of result) {
//                 $(".main-page").append(`<a href="#">${item[2]}</a><br/>`);
//             }
//         },
//         error: (xhr, textStatus, errorThrown) => {
//             console.log(textStatus);
//         }
//     });
// };
const login = () => {
    console.log("dcm Hieu")
    $.ajax({
        url: "http://localhost:9200/user/_search",
        dataType: "JSON",
        method: "get",
        success: data => {
            console.log(data)
            // let bool = 0
            // const name = document.getElementById("name").value
            // const pass = document.getElementById("pass").value
            // for (let i of data) {
            //     if (i.name == name && i.password == pass) {
            //         bool = 1
            //         break;
            //     }
            // }
            // if (bool == 1) {
            //     location.replace("./index.html")
            // }
            // else {
            //     window.alert("Vui lòng nhập lại !")
            // }
        },
        error: (xhr, textStatus, errorThrown) => {
            console.log(textStatus);
        }
    })
}