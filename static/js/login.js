const loginForm = document.querySelector("#login-form");
const statusMessage = document.querySelector("#status");

loginForm.addEventListener("submit", async (event) => {
    event.preventDefault();

    const response = await fetch("/api/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "same-origin",
        body: JSON.stringify({
            username: document.querySelector("#username").value,
            password: document.querySelector("#password").value,
        }),
    });

    const result = await response.json();

    if (!response.ok) {
        statusMessage.textContent = result.error;
        return;
    }

    window.location.href = "/dashboard";
});
