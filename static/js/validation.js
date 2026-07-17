// =============================================
// TaskFlow - Form Validation
// =============================================

document.addEventListener('DOMContentLoaded', function() {

    // Validate registration form
    const registerForm = document.querySelector('form[action*="register"]');
    if (registerForm) {
        registerForm.addEventListener('submit', function(e) {
            const password = this.querySelector('input[name="password"]');
            const confirm = this.querySelector('input[name="confirm_password"]');
            if (password && confirm && password.value !== confirm.value) {
                e.preventDefault();
                alert('Passwords do not match!');
            }
        });
    }

    // Validate change password form
    const passwordForm = document.querySelector('form[action*="change-password"]');
    if (passwordForm) {
        passwordForm.addEventListener('submit', function(e) {
            const newPass = this.querySelector('input[name="new_password"]');
            const confirmPass = this.querySelector('input[name="confirm_password"]');
            if (newPass && confirmPass && newPass.value !== confirmPass.value) {
                e.preventDefault();
                alert('New passwords do not match!');
            }
        });
    }

});