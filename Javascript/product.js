const showMenu = () =>{
    const menu = document.getElementById('menu-bar')
    const nav = document.getElementsByClassName('navbar')[0]
    if(nav.classList.contains('hide')){
        nav.classList.remove('hide')
        nav.classList.add('show')
    }
    else{
        nav.classList.remove('show')
        nav.classList.add('hide')
    }
}
