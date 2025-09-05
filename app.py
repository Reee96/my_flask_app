from flask import Flask, render_template, request, redirect, url_for, session
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

app = Flask(__name__)
app.secret_key = os.environ.get("SECRET_KEY", "dev_secret_key")

# メール情報（Render環境変数で設定）
EMAIL_ADDRESS = os.environ.get("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.environ.get("EMAIL_PASSWORD")
TO_ADDRESS = os.environ.get("TO_ADDRESS")  # 受信先アドレス
PAGE_PASSWORD = os.environ.get("PAGE_PASSWORD", "mypassword")  # ページ保護用パスワード

@app.route("/login", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        password = request.form.get("password")
        if password == PAGE_PASSWORD:
            session["authenticated"] = True
            return redirect(url_for("index"))
        else:
            error = "パスワードが違います"
    return render_template("login.html", error=error)

@app.route("/", methods=["GET", "POST"])
def index():
    if not session.get("authenticated"):
        return redirect(url_for("login"))

    message_sent = False
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        # メール本文作成
        msg = MIMEMultipart()
        msg["From"] = EMAIL_ADDRESS
        msg["To"] = TO_ADDRESS
        msg["Subject"] = f"お問い合わせフォーム: {name}"
        body = f"名前: {name}\nメール: {email}\nメッセージ:\n{message}"
        msg.attach(MIMEText(body, "plain"))

        try:
            with smtplib.SMTP_SSL("smtp.gmail.com", 465) as server:
                server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
                server.send_message(msg)
            message_sent = True
        except Exception as e:
            print("メール送信エラー:", e)
            message_sent = False

    return render_template("index.html", message_sent=message_sent)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
