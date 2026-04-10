document.addEventListener("DOMContentLoaded", function () {
    const token = document.cookie.split("; ").find(r => r.startsWith("csrftoken="))?.split("=")[1];
    if (!token) return;
    document.querySelectorAll("form").forEach(form => {
        form.addEventListener("submit", function (e) {
            e.preventDefault();
            const data = new FormData(form);
            fetch(form.action || window.location.href, {
                method: form.method || "POST",
                headers: { "x-csrftoken": token },
                body: data,
                redirect: "follow"
            }).then(res => {
                if (res.redirected) {
                    window.location.href = res.url;
                } else {
                    res.text().then(html => {
                        document.documentElement.innerHTML = html;
                    });
                }
            }).catch(() => {
                alert("Something went wrong. Please try again.");
            });
        });
    });
});
