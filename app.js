const mobileMenu = document.querySelector('.mobile-menu');
const navToggle = document.querySelector('.mobile-menu-toggle');

navToggle.addEventListener('click', () => {
    const visibility = navToggle.getAttribute("data-visible");

    if (visibility === "false") {
        mobileMenu.setAttribute("data-visible", true);
    }
})