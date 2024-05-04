document.addEventListener("DOMContentLoaded", () => {
    const productContainers = document.querySelectorAll('.product_box');

    productContainers.forEach(container => {
        const quantityInput = container.querySelector('.quantityInput');
        const maxQuantity = parseInt(quantityInput.getAttribute('data-max'));
        const decreaseBtn = container.querySelector('.decrease-btn');
        const increaseBtn = container.querySelector('.increase-btn');
        const productPriceElem = container.querySelector('.product_price');

        if (decreaseBtn && increaseBtn && productPriceElem) {
            const productPrice = parseInt(productPriceElem.textContent.replace(/[^\d.]/g, ''));
            updateTotalPrice(parseInt(quantityInput.value), productPrice, productPriceElem)
            decreaseBtn.addEventListener('click', () => decreaseQuantity(quantityInput, productPrice, productPriceElem));
            increaseBtn.addEventListener('click', () => increaseQuantity(quantityInput, maxQuantity, productPrice, productPriceElem));
        }
    });
});


function decreaseQuantity(inputElement, productPrice, productPriceElem) {
    let currentQuantity = parseInt(inputElement.value);
    if (currentQuantity > 1) {
        currentQuantity--;
        inputElement.value = currentQuantity;
        updateTotalPrice(currentQuantity, productPrice, productPriceElem);
    }
}

function increaseQuantity(inputElement, max, productPrice, productPriceElem) {
    let currentQuantity = parseInt(inputElement.value);
    if (currentQuantity < max) {
        currentQuantity++;
        inputElement.value = currentQuantity;
        updateTotalPrice(currentQuantity, productPrice, productPriceElem);
    }
}

function updateTotalPrice(quantity, productPrice, productPriceElem) {
    productPriceElem.textContent = productPrice * quantity + ' ֏';
    try {
        document.getElementById('checkout-quantity').value = quantity;
    } catch (TypeError) {}
}