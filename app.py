from flask import Flask, render_template, request, redirect, url_for, make_response
from datetime import datetime

app = Flask(__name__)

BANK_STATE = {
    "account_name": "Sailendra Demo Account",
    "balance": 25000,
    "transactions": []
}


def log_tx(action, amount, note):
    BANK_STATE["transactions"].insert(0, {
        "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "action": action,
        "amount": amount,
        "note": note
    })


@app.route("/")
def home():
    return redirect(url_for("bank"))


@app.route("/bank")
def bank():
    return render_template("bank.html", bank=BANK_STATE)


@app.route("/withdraw")
def withdraw():
    return render_template("withdraw.html", bank=BANK_STATE)


@app.route("/withdraw-protected")
def withdraw_protected():
    response = make_response(render_template("withdraw_protected.html", bank=BANK_STATE))
    response.headers["X-Frame-Options"] = "DENY"
    response.headers["Content-Security-Policy"] = "frame-ancestors 'none';"
    return response


@app.route("/process-withdraw", methods=["POST"])
def process_withdraw():
    mode = request.form.get("mode", "custom")

    if mode == "all":
        if BANK_STATE["balance"] > 0:
            amount = BANK_STATE["balance"]
            BANK_STATE["balance"] = 0
            log_tx("WITHDRAW_ALL", amount, "Misleading click triggered full withdrawal")
        return redirect(url_for("bank"))

    try:
        amount = int(request.form.get("amount", "0"))
    except ValueError:
        amount = 0

    if amount > 0 and amount <= BANK_STATE["balance"]:
        BANK_STATE["balance"] -= amount
        log_tx("WITHDRAW_CUSTOM", amount, "User initiated custom withdraw")

    return redirect(url_for("bank"))


@app.route("/reset", methods=["POST"])
def reset():
    BANK_STATE["balance"] = 25000
    BANK_STATE["transactions"] = []
    return redirect(url_for("bank"))


if __name__ == "__main__":
    app.run(debug=True)