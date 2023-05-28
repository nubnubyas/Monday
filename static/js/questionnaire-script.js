const accommodationPriceInput = document.getElementById('accommodation-price');
const accommodationPriceOutput = document.getElementById('accommodation-price-output');
accommodationPriceOutput.innerText = '$' + accommodationPriceInput.value;
accommodationPriceInput.addEventListener('input', () => {
	accommodationPriceOutput.innerText = '$' + accommodationPriceInput.value;
});

const transportationBudgetInput = document.getElementById('transportation-budget');
const transportationBudgetOutput = document.getElementById('transportation-budget');