from flask import Flask, request, redirect
import os

app = Flask(__name__)
DATA_PATH = "/data/notes.txt"
APP_TITLE = os.getenv("APP_TITLE", "K8s Note App")

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        note = request.form.get("note", "")
        with open(DATA_PATH, "a") as f:
            f.write(note + "\n")
        return redirect("/")

    notes = []
    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, "r") as f:
            notes = f.readlines()
    return f"""
        <h1>{APP_TITLE}</h1>
        <form method="post">
            <textarea name="note" rows="4" cols="50" placeholder="Write your 
note here..."></textarea><br>
            <input type="submit" value="Add Note">
        </form>
        <h2>Saved Notes:</h2>
        <ul>{"".join(f"<li>{note.strip()}</li>" for note in notes)}</ul>
    """

if __name__ == "__main__":
    os.makedirs(os.path.dirname(DATA_PATH), exist_ok=True)
    app.run(host="0.0.0.0", port=5000)


