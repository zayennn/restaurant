// Toggle password visibility
document.querySelectorAll('.toggle-password').forEach(button => {
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

// Form validation
document.querySelector('form').addEventListener('submit', function (e) {
    const password = document.getElementById('password').value;
    const confirmPassword = document.getElementById('confirm_password').value;

    if (password !== confirmPassword) {
        e.preventDefault();
        alert('Password and confirmation password do not match!');
    }
});


// menus
// Image Preview Functionality
const menuImage = document.getElementById('menu_image');
const imagePreview = document.getElementById('imagePreview');

if (menuImage && imagePreview) {
    menuImage.addEventListener('change', function () {
        const file = this.files[0];
        if (file) {
            const reader = new FileReader();

            reader.addEventListener('load', function () {
                const previewImage = imagePreview.querySelector('.image-preview__image');
                previewImage.src = this.result;
                imagePreview.classList.add('active');
            });

            reader.readAsDataURL(file);
        }
    });
}

// Format Price Input
const priceInput = document.getElementById('price');
if (priceInput) {
    priceInput.addEventListener('input', function () {
        // Remove non-numeric characters
        this.value = this.value.replace(/[^0-9]/g, '');
    });
}