from flask import Flask, render_template, request
import psycopg2
import os

app = Flask(__name__)

DB_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DB_URL, sslmode="require")
    return conn

@app.route("/", methods=["GET", "POST"])
def index():
    message_sent = False
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        # DB接続（今はコメントアウトしてもOK）
        # conn = get_db_connection()
        # cur = conn.cursor()
        # cur.execute("INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)",
        #             (name, email, message))
        # conn.commit()
        # cur.close()
        # conn.close()

        message_sent = True

    return render_template("index.html", message_sent=message_sent)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
