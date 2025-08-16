document.addEventListener('DOMContentLoaded', function() {
    // Focus on the input field when question page loads
    const inputField = document.querySelector('input[type="number"]');
    if (inputField) {
        inputField.focus();
    }
    
    // Prevent form submission on enter key for number inputs
    const numberInputs = document.querySelectorAll('input[type="number"]');
    numberInputs.forEach(input => {
        input.addEventListener('keydown', function(e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                const form = this.closest('form');
                if (form) {
                    const submitButton = form.querySelector('button[type="submit"]');
                    if (submitButton) {
                        submitButton.click();
                    }
                }
            }
        });
    });
});