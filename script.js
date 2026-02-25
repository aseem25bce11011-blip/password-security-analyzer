function checkPassword() {
    const password = document.getElementById("password").value;

    fetch("/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ password: password })
    })
    .then(response => response.json())
    .then(data => {

        document.getElementById("score").innerText = data.score;
        document.getElementById("strength").innerText = data.strength;
        document.getElementById("crackTime").innerText = data.crack_time;
        document.getElementById("entropy").innerText = data.entropy;

        let fill = document.getElementById("strength-fill");
        fill.style.width = data.score + "%";

        if (data.strength === "Weak") {
            fill.style.background = "red";
        } else if (data.strength === "Medium") {
            fill.style.background = "orange";
        } else {
            fill.style.background = "green";
        }

        let suggestionsList = document.getElementById("suggestions");
        suggestionsList.innerHTML = "";

        data.suggestions.forEach(suggestion => {
            let li = document.createElement("li");
            li.innerText = suggestion;
            suggestionsList.appendChild(li);
        });
    });
}

function togglePassword() {
    const input = document.getElementById("password");
    input.type = input.type === "password" ? "text" : "password";
}