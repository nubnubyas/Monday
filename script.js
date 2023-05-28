// Code for navigation menu
const navToggle = document.querySelector('.nav-toggle');
const navLinks = document.querySelectorAll('.nav__link');

navToggle.addEventListener('click', () => {
	document.body.classList.toggle('nav-open');
});

navLinks.forEach(link => {
	link.addEventListener('click', () => {
		document.body.classList.remove('nav-open');
	});
});

// Code for group thumbnails
const groupThumbnails = document.querySelectorAll('#groups li');

groupThumbnails.forEach(thumbnail => {
	thumbnail.addEventListener('click', () => {
		window.location.href = thumbnail.querySelector('a').getAttribute('href');
	});
});