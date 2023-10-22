const navbtn = document.getElementById('nav-btn');
const navinput = document.getElementById('nav-input');
const headtext = document.getElementById('head-text');
const headtext2 = document.getElementById('head-text2');
const headerinput = document.getElementById('header-input');
const search_form = document.getElementById('search-form');
const nav_search_form = document.getElementById('nav-search-form');

const cngNavElemets = (e) => {
    navbtn.innerText = e
    navinput.placeholder = `Enter ${e}`
    if (navbtn.innerText == 'Company') {
        nav_search_form.action = '/search-address'
    } else {
        nav_search_form.action = '/search-employee'
    }
}
const cngHeadText = () => {
    if (headtext2.innerText == 'Find your perfect Company today!') {
        headtext2.innerText = 'Find your perfect Employee today!'
        headerinput.placeholder = 'Enter company name'
        search_form.action = '/search-address'
    }
    else {
        headtext2.innerText = 'Find your perfect Company today!'
        headerinput.placeholder = 'Enter Employee name'
        search_form.action = '/search-employee'
    }

}

// check if search-address in url
const url = window.location.href;
if (url.includes('search-address')) {
    cngNavElemets('Address')
}