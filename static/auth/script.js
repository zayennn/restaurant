document.addEventListener('DOMContentLoaded', function () {
    // Toggle password visibility
    const togglePasswordButtons = document.querySelectorAll('.toggle-password');
    togglePasswordButtons.forEach(button => {
        button.addEventListener('click', function () {
            const input = this.parentElement.querySelector('input');
            const icon = this.querySelector('i');

            if (input.type === 'password') {
                input.type = 'text';
                icon.classList.remove('fa-eye');
                icon.classList.add('fa-eye-slash');
            } else {
                input.type = 'password';
                icon.classList.remove('fa-eye-slash');
                icon.classList.add('fa-eye');
            }
        });
    });

    // Password strength indicator (for register page)
    const passwordInput = document.getElementById('password');
    if (passwordInput) {
        passwordInput.addEventListener('input', function () {
            const strengthBars = document.querySelectorAll('.strength-bar');
            const strengthText = document.querySelector('.strength-text');
            const password = this.value;

            // Reset
            strengthBars.forEach(bar => {
                bar.style.backgroundColor = '#eee';
            });

            // Check password strength
            let strength = 0;

            // Length
            if (password.length >= 8) strength++;
            if (password.length >= 12) strength++;

            // Complexity
            if (/[A-Z]/.test(password)) strength++;
            if (/[0-9]/.test(password)) strength++;
            if (/[^A-Za-z0-9]/.test(password)) strength++;

            // Update UI
            if (password.length === 0) {
                strengthText.textContent = 'Password strength';
            } else {
                for (let i = 0; i < Math.min(strength, 3); i++) {
                    let color;
                    if (strength <= 2) color = '#ff4757'; // Weak
                    else if (strength <= 4) color = '#ffa502'; // Medium
                    else color = '#2ed573'; // Strong

                    strengthBars[i].style.backgroundColor = color;
                }

                if (strength <= 2) strengthText.textContent = 'Weak';
                else if (strength <= 4) strengthText.textContent = 'Medium';
                else strengthText.textContent = 'Strong';
            }
        });
    }
});