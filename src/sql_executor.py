import sqlite3
def execute_sql(db_id, sql_query):
    file_path = f"database/{db_id}/{db_id}.sqlite"
    connection = sqlite3.connect(file_path)
    cursor = connection.cursor()
    try:
        cursor.execute(sql_query)
        result = cursor.fetchall()
        connection.close()
        return result
    except sqlite3.OperationalError as e:
        connection.close()
        return {"error": str(e)}
