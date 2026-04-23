/**
 * Snappito Theme Engine
 * Optimized for instant logo swapping and global theme synchronization.
 */
(function() {
    function applyTheme(theme) {
        document.body.classList.toggle('dark-mode', theme === 'dark');
        localStorage.setItem('theme', theme);

        const themeToggle = document.getElementById('theme-toggle');
        if (themeToggle) {
            themeToggle.innerHTML = `<span class="icon">${theme === 'dark' ? '☀️' : '🌙'}</span>`;
        }

        // Global Logo Update
        const logos = document.querySelectorAll('#main-logo, #nav-logo');
        logos.forEach(logo => {
            if (theme === 'dark') {
                logo.src = 'src/assets/images/logo_dark.png';
            } else {
                logo.src = 'src/assets/images/logo_white_bg.png';
            }
        });

        // Footer Logo
        const footerLogo = document.getElementById('footer-logo');
        if (footerLogo) {
            footerLogo.src = 'src/assets/images/logo_white_bg.png';
        }
    }

    function init() {
        const themeToggle = document.getElementById('theme-toggle');
        const currentTheme = localStorage.getItem('theme') || 'light';
        
        // Initial application
        applyTheme(currentTheme);

        if (themeToggle) {
            themeToggle.addEventListener('click', (e) => {
                e.preventDefault();
                const newTheme = document.body.classList.contains('dark-mode') ? 'light' : 'dark';
                applyTheme(newTheme);
            });
        }
    }

    // Run as soon as DOM is ready or if already ready
    if (document.readyState === 'loading') {
        document.addEventListener('DOMContentLoaded', init);
    } else {
        init();
    }

    // Export for external access if needed
    window.SnappitoTheme = { apply: applyTheme };
})();
