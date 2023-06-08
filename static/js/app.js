const mobileMenu = document.querySelector('.mobile-menu');
const mobileMenuOpen = document.querySelector('.mobile-menu-toggle');
const mobileMenuClose = document.querySelector('.mobile-menu-toggle-close');

mobileMenuOpen.addEventListener('click', () => {
    const visibility = mobileMenu.getAttribute("data-visible");

    if (visibility === "false") {
        mobileMenu.setAttribute("data-visible", true);
        mobileMenuOpen.setAttribute("aria-expanded", true);
        document.querySelector("body").classList.add("fixed-position");
    }
});

mobileMenuClose.addEventListener('click', () => {
    const visibility = mobileMenu.getAttribute("data-visible");

    if (visibility === "true") {
        mobileMenu.setAttribute("data-visible", false);
        mobileMenuOpen.setAttribute("aria-expanded", false);
        document.querySelector("body").classList.remove("fixed-position");
    }
});