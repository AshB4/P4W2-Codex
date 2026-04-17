from flask import Flask, request, jsonify
import psycopg2

app = Flask(__name__)


# DB connection function
def get_connection():
    return psycopg2.connect(
        host="pathway-4.ca1yc8okmo57.us-east-1.rds.amazonaws.com",
        database="db_ashley",
        user="ashley",
        password="ashley_pass",
        port="5432",
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
