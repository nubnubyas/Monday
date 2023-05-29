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

// for questionnaire
const accommodationPriceInput = document.getElementById('accommodation-price');
const accommodationPriceOutput = document.getElementById('accommodation-price-output');
accommodationPriceOutput.innerText = '$' + accommodationPriceInput.value;
accommodationPriceInput.addEventListener('input', () => {
	accommodationPriceOutput.innerText = '$' + accommodationPriceInput.value;
});

const transportationBudgetInput = document.getElementById('transportation-budget');
const transportationBudgetOutput = document.getElementById('transportation-budget');

function joinGroup() {
	var groupId = document.getElementById("group-id").value;
	var password = document.getElementById("password").value;
	// TODO: Implement logic to join the group with the given ID and password
	alert(`You are now a member of group ${groupId}!`);
}

function createGroup() {
	var groupName = document.getElementById("group-name").value;
	var destination = document.getElementById("destination").value;
	var date = document.getElementById("date").value;
	var groupPassword = document.getElementById("group-password").value;
	// TODO: Implement logic to create a new group with the given information
	alert(`Group "${groupName}" created successfully!`);
}

function copyLink() {
	var link = document.getElementById("link");
	link.select();
	link.setSelectionRange(0, 99999);
	document.execCommand("copy");
	alert("Link copied to clipboard!");
}