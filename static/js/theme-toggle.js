// theme-toggle.js
document.addEventListener('DOMContentLoaded', function () {
    const themeSwitch = document.getElementById('themeSwitch');

    // Add event listener for theme switch changes
    themeSwitch.addEventListener('change', function () {
        const newTheme = themeSwitch.checked ? 'dark' : 'light';

        // Apply the new theme
        document.body.classList.remove('light', 'dark');
        document.body.classList.add(newTheme);

        // Update navbar classes
        const navbar = document.querySelector('nav');
        navbar.classList.remove('navbar-dark', 'bg-dark', 'navbar-light', 'bg-light');
        if (newTheme === 'dark') {
            navbar.classList.add('navbar-dark', 'bg-dark');
        } else {
            navbar.classList.add('navbar-light', 'bg-light');
        }

        // Send the new theme to the backend
        fetch('/set-theme', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ theme: newTheme }),
        }).then((response) => response.json())
          .then((data) => {
              // Save the theme in localStorage to persist across sessions
              localStorage.setItem('theme', newTheme);
          });
    });
});