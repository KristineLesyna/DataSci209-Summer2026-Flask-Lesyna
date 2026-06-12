from flask import Flask, render_template, jsonify, request
import pandas as pd
import os
import sqlite3

app = Flask(__name__)

APP_FOLDER = os.path.dirname(os.path.realpath(__file__))

@app.route("/")
def hello():
    return render_template("index.html")

@app.route("/getData/<int:year>")
def getData(year):
    revenue = pd.read_csv(os.path.join(APP_FOLDER, "static/data/1_Revenues.csv"))

    if year < 1942 or year > 2008:
        return "Error in the year range"

    filteredRevenue = revenue[
        revenue["Year4"] == year
    ][["Name", "Year4", "Total Revenue", "Population (000)"]]

    return filteredRevenue.to_json(orient="records")

@app.route("/api")
def api():
    return jsonify({"x": 77})

@app.route("/players/count")
def players_count():
    conn = sqlite3.connect(os.path.join(APP_FOLDER, "players_20.db"))
    cursor = conn.cursor()

    cursor.execute("SELECT COUNT(*) FROM players")
    count = cursor.fetchone()[0]

    conn.close()

    return jsonify({"count": count})

@app.route("/players/get_nationality")
def get_nationality():
    player = request.args.get("player")

    conn = sqlite3.connect(os.path.join(APP_FOLDER, "players_20.db"))
    cursor = conn.cursor()

    cursor.execute(
        "SELECT nationality FROM players WHERE short_name = ?",
        (player,)
    )

    result = cursor.fetchone()
    conn.close()

    return jsonify({"nationality": result[0]})

if __name__ == "__main__":
    app.run()