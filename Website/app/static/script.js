// Select the header, logo, and profile icon elements
const header = document.querySelector("header");
const logo = document.getElementById("logo");
const profileIcon = document.getElementById('profile-icon');

// Define the scroll function
function scrollFunction() {
  if (document.body.scrollTop > 50 || document.documentElement.scrollTop > 50) {
    header.classList.add("scrolled");
    logo.classList.add("scrolled");
    profileIcon.classList.add('scrolled');
  } else {
    header.classList.remove("scrolled");
    logo.classList.remove("scrolled");
    profileIcon.classList.remove('scrolled');
  }
}

// Attach the scroll function to the window scroll event
window.onscroll = scrollFunction;

// Add click event listener to the user profile
document.querySelector('.user-profile').addEventListener('click', function() {
  document.querySelector('.dropdown-menu').style.display = 'block';
});

// Opens overlay when container is clicked
function onContainerClick() {
  document.getElementById('overlay').style.display = 'block';
}

// Closes overlay when overlay is clicked
function onOverlayClick() {
  document.getElementById('overlay').style.display = 'none';
}