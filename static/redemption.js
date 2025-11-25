document.addEventListener("DOMContentLoaded", () => {
    const paymentSelect = document.getElementById("payment_method");
    const cardSection = document.getElementById("cardSection");

    // Hide card section by default
    cardSection.classList.add("hidden");

    paymentSelect.addEventListener("change", function () {
        if (this.value === "card") {
            cardSection.classList.remove("hidden");
        } else {
            cardSection.classList.add("hidden");
        }
    });

    // Optional extra validation (you can remove if unnecessary)
    document.getElementById("redemptionForm").addEventListener("submit", function (e) {
        if (paymentSelect.value === "card") {
            const cardNum = document.getElementById("card_number").value.trim();
            const cvv = document.getElementById("cvv").value.trim();

            if (cardNum.length < 16 || isNaN(cardNum)) {
                alert("Please enter a valid 16-digit card number.");
                e.preventDefault();
                return;
            }

            if (cvv.length < 3 || isNaN(cvv)) {
                alert("Please enter a valid 3-digit CVV.");
                e.preventDefault();
                return;
            }
        }
    });
});
