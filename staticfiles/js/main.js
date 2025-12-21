document.addEventListener('DOMContentLoaded', function() {
    const headerWrapper = document.querySelector('.header-wrapper');
    const navbar = document.getElementById('navbar');
    const donateForm = document.getElementById('donateForm');

    function handleStickyHeader() {
        if (window.scrollY > 50) {
            headerWrapper.classList.add('sticky');
            if (navbar) {
                navbar.classList.add('sticky');
            }
        } else {
            headerWrapper.classList.remove('sticky');
            if (navbar) {
                navbar.classList.remove('sticky');
            }
        }
    }

    window.addEventListener('scroll', handleStickyHeader);
    handleStickyHeader();

    if (donateForm) {
        donateForm.addEventListener('submit', function(e) {
            const amount = document.getElementById('amount').value;
            if (amount && parseFloat(amount) > 0) {
                if (!confirm('Are you sure you want to donate $' + parseFloat(amount).toFixed(2) + '?')) {
                    e.preventDefault();
                }
            }
        });
    }

    const buttons = document.querySelectorAll('.btn');
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-2px)';
        });
        button.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    const projectCards = document.querySelectorAll('.project-card');
    projectCards.forEach(card => {
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-8px)';
        });
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0)';
        });
    });

    const navLinks = document.querySelectorAll('.nav-links a, .footer-nav a');
    navLinks.forEach(link => {
        link.addEventListener('click', function() {
            const href = this.getAttribute('href');
            if (href && href.startsWith('#')) {
                const target = document.querySelector(href);
                if (target) {
                    target.scrollIntoView({ behavior: 'smooth' });
                }
            }
        });
    });
});
