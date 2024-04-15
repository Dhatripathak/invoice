document.addEventListener('DOMContentLoaded', function () {
    const taxForm = document.getElementById('taxForm');
    const ageInput = document.getElementById('age');
    const incomeInput = document.getElementById('income');
    const deductionsInput = document.getElementById('deductions');

    taxForm.addEventListener('submit', function (event) {
        event.preventDefault();
        if (taxForm.checkValidity()) {
            // Calculate tax and show result
            const tax = calculateTax(ageInput.value, parseFloat(incomeInput.value), parseFloat(deductionsInput.value));
            showResult(tax);
        } else {
            taxForm.classList.add('was-validated');
        }
    });

    function calculateTax(age, income, deductions) {
        let tax = 0;
        if (income - deductions > 8) {
            if (age === '<40') {
                tax = 0.3 * (income - deductions - 8);
            } else if (age === '≥40 & <60') {
                tax = 0.4 * (income - deductions - 8);
            } else if (age === '≥60') {
                tax = 0.1 * (income - deductions - 8);
            }
        }
        return tax;
    }

    function showResult(tax) {
        const resultModal = new bootstrap.Modal(document.getElementById('modal')); // Updated ID here
        const modalBody = document.querySelector('#modal .modal-body'); // Updated ID here
        modalBody.innerHTML = `<p>Tax to be paid: ${tax} Lakhs</p>`;
        resultModal.show();
    }
});
