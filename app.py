from flask import Flask, render_template, request, jsonify
import re
import math

app = Flask(__name__)

COMMON_WORDS = ["password", "123456", "qwerty", "admin", "welcome", "login"]

def analyze_password(password):
    score = 0
    suggestions = []
    length = len(password)

    # -------- Basic Checks --------

    if length >= 8:
        score += 20
    else:
        suggestions.append("Use at least 8 characters.")

    if re.search(r"[A-Z]", password):
        score += 15
    else:
        suggestions.append("Add uppercase letters.")

    if re.search(r"[a-z]", password):
        score += 15
    else:
        suggestions.append("Add lowercase letters.")

    if re.search(r"[0-9]", password):
        score += 15
    else:
        suggestions.append("Add numbers.")

    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        score += 15
    else:
        suggestions.append("Add special characters.")

    # -------- Common Words --------

    for word in COMMON_WORDS:
        if word in password.lower():
            score -= 20
            suggestions.append("Avoid common words like 'password'.")

    # -------- Repeated Characters --------

    if re.search(r"(.)\1\1", password):
        score -= 10
        suggestions.append("Avoid repeated characters.")

    # -------- Dictionary-like Word Detection --------
    # Entire password is only letters (like india, rahul, computer)

    if re.search(r"^[A-Za-z]{4,}$", password):
        score -= 20
        suggestions.append("Avoid using dictionary words as passwords.")

    # -------- Name Pattern Detection --------
    # Capitalized name followed by numbers (Rahul123)

    if re.search(r"^[A-Z][a-z]+[0-9]*$", password):
        score -= 15
        suggestions.append("Avoid using common names with numbers.")

    # -------- Year Detection (1900–2029) --------

    if re.search(r"(19[0-9]{2}|20[0-2][0-9])", password):
        score -= 10
        suggestions.append("Avoid using birth years or common years.")

    # -------- Clamp Score --------

    score = max(0, min(score, 100))

    # -------- Strength Label --------

    if score < 40:
        strength = "Weak"
    elif score < 70:
        strength = "Medium"
    else:
        strength = "Strong"

    # -------- Entropy Calculation --------

    charset = 0
    if re.search(r"[a-z]", password):
        charset += 26
    if re.search(r"[A-Z]", password):
        charset += 26
    if re.search(r"[0-9]", password):
        charset += 10
    if re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        charset += 32

    entropy = length * math.log2(charset) if charset > 0 else 0

    # -------- Crack Time Estimation --------

    guesses_per_second = 1_000_000_000  # 1 billion guesses/sec
    seconds = (2 ** entropy) / guesses_per_second if entropy > 0 else 0

    if seconds < 60:
        crack_time = f"{seconds:.2f} seconds"
    elif seconds < 3600:
        crack_time = f"{seconds/60:.2f} minutes"
    elif seconds < 86400:
        crack_time = f"{seconds/3600:.2f} hours"
    elif seconds < 31536000:
        crack_time = f"{seconds/86400:.2f} days"
    else:
        crack_time = f"{seconds/31536000:.2f} years"

    return score, strength, crack_time, suggestions, round(entropy, 2)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/check", methods=["POST"])
def check():
    data = request.json
    password = data.get("password", "")

    score, strength, crack_time, suggestions, entropy = analyze_password(password)

    return jsonify({
        "score": score,
        "strength": strength,
        "crack_time": crack_time,
        "suggestions": suggestions,
        "entropy": entropy
    })


if __name__ == "__main__":
    app.run(debug=True)