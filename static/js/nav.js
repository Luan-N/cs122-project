const logoutButton = document.querySelector("#nav-logout");

if (logoutButton) {
    logoutButton.addEventListener("click", async () => {
        await fetch("/api/logout", {
            method: "POST",
            credentials: "same-origin",
        });

        window.location.href = "/login";
    });
}
