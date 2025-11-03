

document.addEventListener('DOMContentLoaded', function () {
    const menuContainer = document.querySelector('.menu-container');
    const openMenuBtn = document.querySelector('.button-show-menu');
    const closeMenuBtn = document.querySelector('.button-close-menu');

    if (openMenuBtn && menuContainer) {
        openMenuBtn.addEventListener('click', function () {
            menuContainer.style.width = '260px';
            menuContainer.classList.remove('menu-hidden');
            menuContainer.classList.add('menu-visible');
        });
    }

    if (closeMenuBtn && menuContainer) {
        closeMenuBtn.addEventListener('click', function () {
            menuContainer.classList.remove('menu-visible');
            menuContainer.classList.add('menu-hidden');
            menuContainer.style.width = '';
        });
    }
});