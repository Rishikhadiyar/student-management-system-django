// Local static JS to demonstrate Django static files setup.
document.addEventListener("DOMContentLoaded", function () {
    // Mobile Menu Toggle
    const menuButton = document.getElementById("mobile-menu-button");
    const navMenu = document.getElementById("nav-menu");

    if (menuButton && navMenu) {
        menuButton.addEventListener("click", function () {
            navMenu.classList.toggle("hidden");
            navMenu.classList.toggle("flex");
        });
    }

    const path = window.location.pathname;
    const links = document.querySelectorAll("nav a[data-nav]");

    links.forEach((link) => {
        const navKey = link.getAttribute("data-nav");
        const isActive =
            (navKey === "home" && path === "/") ||
            (navKey === "create" && path.startsWith("/create")) ||
            (navKey === "students" && path.startsWith("/students")) ||
            (navKey === "dashboard" && path.startsWith("/dashboard")) ||
            (navKey === "course-add" && path.startsWith("/courses/add")) ||
            (navKey === "login" && path.startsWith("/login")) ||
            (navKey === "register" && path.startsWith("/register"));

        if (isActive) {
            link.classList.add("ring-2", "ring-emerald-200");
        }
    });
});
