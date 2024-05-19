// Select the header, logo, and profile icon elements
const header = document.querySelector("header");
const logo = document.getElementById("logo");
const profileIcon = document.getElementById('profile-icon');
const flashedMessages = document.getElementById('flashedMessages');
const dropdownMenu = document.querySelector('.dropdown-menu');

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

// Toggle the dropdown menu visibility on profile icon click
profileIcon.addEventListener('click', function() {
  if (dropdownMenu.style.display === 'block') {
    dropdownMenu.style.display = 'none';
  } else {
    dropdownMenu.style.display = 'block';
  }
});

// Hide dropdown menu when clicking outside
document.addEventListener('click', function(event) {
  if (!profileIcon.contains(event.target) && !dropdownMenu.contains(event.target)) {
    dropdownMenu.style.display = 'none';
  }
});

// Hide flashed messages if there are none after the page loads
window.addEventListener('load', function() {
  if (flashedMessages && flashedMessages.innerHTML.trim() === '') {
    flashedMessages.style.display = 'none';
  }
});
