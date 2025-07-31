document.addEventListener('DOMContentLoaded', function () {
    // Navigation between sections
    const navLinks = document.querySelectorAll('.sidebar-nav a');
    const contentSections = document.querySelectorAll('.content-section');

    navLinks.forEach(link => {
        link.addEventListener('click', function (e) {
            e.preventDefault();

            // Remove active class from all links and sections
            navLinks.forEach(navLink => navLink.parentElement.classList.remove('active'));
            contentSections.forEach(section => section.classList.remove('active'));

            // Add active class to clicked link
            this.parentElement.classList.add('active');

            // Show corresponding section
            const target = this.getAttribute('href');
            document.querySelector(target).classList.add('active');
        });
    });

    // Profile navigation tabs
    const profileNavBtns = document.querySelectorAll('.profile-nav-btn');
    const profileTabs = document.querySelectorAll('.profile-tab');

    profileNavBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            // Remove active class from all buttons and tabs
            profileNavBtns.forEach(btn => btn.classList.remove('active'));
            profileTabs.forEach(tab => tab.classList.remove('active'));

            // Add active class to clicked button
            this.classList.add('active');

            // Show corresponding tab
            const target = this.getAttribute('data-target');
            document.getElementById(target).classList.add('active');
        });
    });

    // Menu category tabs
    const categoryBtns = document.querySelectorAll('.category-btn');

    categoryBtns.forEach(btn => {
        btn.addEventListener('click', function () {
            categoryBtns.forEach(btn => btn.classList.remove('active'));
            this.classList.add('active');
            // Here you would filter menu items based on category
        });
    });

    // Modal functionality
    const modal = document.getElementById('userModal');
    const addUserBtn = document.getElementById('addUserBtn');
    const closeModal = document.querySelector('.close-modal');
    const cancelBtn = document.querySelector('.cancel-btn');

    if (addUserBtn) {
        addUserBtn.addEventListener('click', function () {
            modal.style.display = 'flex';
        });
    }

    if (closeModal) {
        closeModal.addEventListener('click', function () {
            modal.style.display = 'none';
        });
    }

    if (cancelBtn) {
        cancelBtn.addEventListener('click', function () {
            modal.style.display = 'none';
        });
    }

    window.addEventListener('click', function (e) {
        if (e.target === modal) {
            modal.style.display = 'none';
        }
    });

    // Form submissions
    const userForm = document.getElementById('userForm');
    if (userForm) {
        userForm.addEventListener('submit', function (e) {
            e.preventDefault();
            // Here you would handle form submission to add/edit user
            alert('User saved successfully!');
            modal.style.display = 'none';
            this.reset();
        });
    }

    // Logout functionality
    const logoutBtn = document.getElementById('logoutBtn');
    if (logoutBtn) {
        logoutBtn.addEventListener('click', function () {
            if (confirm('Are you sure you want to logout?')) {
                window.location.href = 'login.html';
            }
        });
    }

    // Edit and Delete buttons functionality
    document.querySelectorAll('.action-btn.edit').forEach(btn => {
        btn.addEventListener('click', function () {
            // Here you would implement edit functionality
            // For now, just show the modal with existing data
            modal.style.display = 'flex';
            document.querySelector('.modal h3').textContent = 'Edit User';
        });
    });

    document.querySelectorAll('.action-btn.delete').forEach(btn => {
        btn.addEventListener('click', function () {
            if (confirm('Are you sure you want to delete this item?')) {
                // Here you would implement delete functionality
                const row = this.closest('tr') || this.closest('.seat-card') || this.closest('.menu-item-card');
                if (row) row.remove();
                alert('Item deleted successfully!');
            }
        });
    });

    // Add buttons for other sections
    const addSeatBtn = document.getElementById('addSeatBtn');
    if (addSeatBtn) {
        addSeatBtn.addEventListener('click', function () {
            alert('Add new seat functionality would go here');
        });
    }

    const addMenuBtn = document.getElementById('addMenuBtn');
    if (addMenuBtn) {
        addMenuBtn.addEventListener('click', function () {
            alert('Add new menu item functionality would go here');
        });
    }

    const addReservationBtn = document.getElementById('addReservationBtn');
    if (addReservationBtn) {
        addReservationBtn.addEventListener('click', function () {
            alert('Add new reservation functionality would go here');
        });
    }

    // Profile form submissions
    document.querySelectorAll('.profile-form').forEach(form => {
        form.addEventListener('submit', function (e) {
            e.preventDefault();
            alert('Changes saved successfully!');
        });
    });
});