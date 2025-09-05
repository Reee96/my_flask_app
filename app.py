from flask import Flask, render_template, request
import psycopg2
import os

app = Flask(__name__)

# DB接続情報（Renderで後で設定する環境変数）
DB_URL = os.environ.get("DATABASE_URL")

def get_db_connection():
    conn = psycopg2.connect(DB_URL, sslmode="require")
    return conn

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form["name"]
        email = request.form["email"]
        message = request.form["message"]

        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO messages (name, email, message) VALUES (%s, %s, %s)",
                    (name, email, message))
        conn.commit()
        cur.close()
        conn.close()
        return "送信完了しました！"

    return '''
    <form method="POST">
        名前: <input type="text" name="name"><br>
        メール: <input type="text" name="email"><br>
        メッセージ: <textarea name="message"></textarea><br>
        <input type="submit" value="送信">
    </form>
    '''

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

