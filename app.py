from flask import Flask, jsonify
import sqlite3

app = Flask(__name__)


@app.route("/<int:itemid>")
def get_item(itemid):
    con = sqlite3.connect("animal.db")
    cur = con.cursor()
    query = f"""SELECT * FROM animals_list
                WHERE animal_id = {itemid}"""
    cur.execute(query)
    response = cur.fetchall()

    return jsonify(response)


if __name__ == "__main__":
    app.run(port=8000, debug=True)
