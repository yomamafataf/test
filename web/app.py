from pathlib import Path

from flask import Flask, render_template, request

app = Flask(__name__)

PASSWORD_FILE = Path(__file__).with_name(
    "10-million-password-list-top-1000.txt"
)


def load_common_passwords():
    with PASSWORD_FILE.open(
        encoding="utf-8",
        errors="ignore",
    ) as password_file:
        return {
            line.strip().casefold()
            for line in password_file
            if line.strip()
        }


COMMON_PASSWORDS = load_common_passwords()


def validate_password(password):
    errors = []

    # The historical C6 requirement used 10 characters when MFA was absent.
    if len(password) < 10:
        errors.append("Password must contain at least 10 characters.")

    # Support long passphrases but impose a reasonable upper limit.
    if len(password) > 64:
        errors.append("Password must not exceed 64 characters.")

    # Historical C6 permits printable ASCII characters and spaces.
    if any(ord(character) < 32 or ord(character) > 126
           for character in password):
        errors.append(
            "Password may only contain printable characters and spaces."
        )

    if password.casefold() in COMMON_PASSWORDS:
        errors.append("This password appears in the common-password list.")

    return errors


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        password = request.form.get("password", "")
        errors = validate_password(password)

        if errors:
            return render_template("index.html", errors=errors)

        # Render directly instead of placing the password in the URL.
        return render_template("result.html", password=password)

    return render_template("index.html", errors=[])


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)