import sqlite3

def get_grade_from_db(percentage):

    conn = sqlite3.connect('app/db/grades.db')
    cursor = conn.cursor()


    query = """
        SELECT grade FROM grades.db
        WHERE ? BETWEEN min_percentage and max_percentage
    """

    cursor.execute(query, (percentage,))
    result = cursor.fetchone()
    conn.close()

    if result:
        return result[0]
    
    else:
        return 'F' #Fallback