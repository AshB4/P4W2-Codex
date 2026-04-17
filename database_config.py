import psycopg2

try:
    print("Attempting to connect...")

    connection = psycopg2.connect(
        host="pathway-4.ca1yc8okmo57.us-east-1.rds.amazonaws.com",
        database="db_ashley",
        user="ashley",
        password="ashley_pass",
        port="5432",
    )

    print("Connection established!")

    cursor = connection.cursor()
    print("Running query...")

    cursor.execute("SELECT * FROM persons;")
    rows = cursor.fetchall()

    print("Query successful!")
    print("Rows:", rows)

    cursor.close()
    connection.close()
    print("Connection closed.")

except Exception as e:
    print("ERROR OCCURRED:")
    print(type(e)) 
    print(e) 
