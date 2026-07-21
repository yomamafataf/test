from pathlib import Path
import os
import secrets

from flask import Flask, render_template, request
from flask_wtf.csrf import CSRFProtect

app = Flask(__name__)

app.config["SECRET_KEY"] = (
    os.getenv("FLASK_SECRET_KEY") or secrets.token_hex(32)
)
CSRFProtect(app)

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

    if len(password) < 10:
        errors.append(
            "Password must contain at least 10 characters."
        )

    if len(password) > 64:
        errors.append(
            "Password must not exceed 64 characters."
        )

    if any(
        ord(character) < 32 or ord(character) > 126
        for character in password
    ):
        errors.append(
            "Password may only contain printable characters and spaces."
        )

    if password.casefold() in COMMON_PASSWORDS:
        errors.append(
            "This password appears in the common-password list."
        )

    return errors


@app.route("/", methods=["GET", "POST"])
def home():
    if request.method == "POST":
        password = request.form.get("password", "")
        errors = validate_password(password)

        if errors:
            return render_template(
                "index.html",
                errors=errors,
            )

        return render_template(
            "result.html",
            password=password,
        )

    return render_template(
        "index.html",
        errors=[],
    )


if __name__ == "__main__":
    app.run(
        host=os.getenv("APP_HOST", "127.0.0.1"),
        port=5000,
    )