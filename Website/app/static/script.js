// Select the header and logo elements
const header = document.querySelector("header");
const logo = document.getElementById("logo");

// Define the scroll function
function scrollFunction() {
  if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
    header.classList.add("scrolled");
    logo.classList.add("scrolled");
  } else {
    header.classList.remove("scrolled");
    logo.classList.remove("scrolled");
  }
}


window.onscroll = scrollFunction;

document.querySelector('.user-profile').addEventListener('click', function() {
  document.querySelector('.dropdown-menu').style.display = 'block';
});