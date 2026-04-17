from flask import Flask, request, jsonify
from dotenv import load_dotenv
import psycopg2
import os

load_dotenv()

app = Flask(__name__)


def get_connection():
    return psycopg2.connect(
        host=os.getenv("DB_HOST"),
        database=os.getenv("DB_NAME"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        port=os.getenv("DB_PORT"),
    )


# POST route
@app.route("/add_person", methods=["POST"])
def add_person():
    data = request.get_json()

    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute(
            "INSERT INTO persons (first_name, last_name, address, age) VALUES (%s, %s, %s, %s)",
            (data["first_name"], data["last_name"], data["address"], data["age"]),
        )

        connection.commit()

        cursor.close()
        connection.close()

        return jsonify({"message": "Person added successfully!"}), 201

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# GET route
@app.route("/get_persons", methods=["GET"])
def get_persons():
    try:
        connection = get_connection()
        cursor = connection.cursor()

        cursor.execute("SELECT * FROM persons;")
        rows = cursor.fetchall()

        # convert to list of dicts
        persons = []
        for row in rows:
            persons.append(
                {
                    "id": row[0],
                    "first_name": row[1],
                    "last_name": row[2],
                    "address": row[3],
                    "age": row[4],
                }
            )

        cursor.close()
        connection.close()

        return jsonify(persons)

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True)
