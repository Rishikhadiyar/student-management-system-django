// Local static JS to demonstrate Django static files setup.
document.addEventListener("DOMContentLoaded", function () {
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
