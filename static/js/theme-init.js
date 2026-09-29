(function () {
    var saved = localStorage.getItem("theme");
    var theme = saved || "dark";
    document.documentElement.setAttribute("data-theme", theme);
})();
