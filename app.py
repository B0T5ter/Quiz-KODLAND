from flask import Flask, render_template, request
import sqlite3

app = Flask(__name__)

def get_db():
    return sqlite3.connect("quiz.db")

with get_db() as db:
    cur = db.cursor()
    cur.execute("CREATE TABLE IF NOT EXISTS scores (value INTEGER)")
    db.commit()

@app.route("/", methods=["GET", "POST"])
def quiz():
    score = None
    best_score = 0

    if request.method == "POST":
        answers = {
            "q1": request.form.get("q1"),
            "q2": request.form.get("q2"),
            "q3": request.form.get("q3"),
            "q4": request.form.get("q4")
        }

        correct_answers = {
            "q1": "TensorFlow",
            "q2": "Przetwarzanie języka naturalnego",
            "q3": "CNN",
            "q4": "Operacje na tensorach"
        }

        score = 0
        for key in correct_answers:
            if answers.get(key) == correct_answers[key]:
                score += 1
        score = int(score / 4 * 100)

        db = get_db()
        cur = db.cursor()
        cur.execute("INSERT INTO scores VALUES (?)", (score,))
        db.commit()

    db = get_db()
    cur = db.cursor()
    cur.execute("SELECT MAX(value) FROM scores")
    best_score = cur.fetchone()[0] or 0

    return render_template("quiz.html", score=score, best_score=best_score)

if __name__ == "__main__":
    app.run(debug=True)
