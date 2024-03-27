import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT
import os

def get_db_connection():
    conn = psycopg2.connect(os.getenv("POSTGRES_CONNECTION_STRING"))
    # Use this to execute statement w/out commiting in the code
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  
    return conn


# Local Testing...

# def get_db_connection():
#     conn = psycopg2.connect(database="test", 
#                              user="postgres", 
#                              host='localhost',
#                              password="waterpop",
#                              port=5432)
#     # Use this to execute statement w/out commiting in the code
#     conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)  
#     return conn

def create_table():
    conn = get_db_connection()
    cursor = conn.cursor()
    create_table_query = '''
    CREATE TABLE IF NOT EXISTS survey (
        id                  SERIAL PRIMARY KEY,
        survey_date         TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP,
        name                TEXT,
        frequency           TEXT,
        age                 TEXT,
        meal_time           TEXT,
        restaurant          BOOLEAN,
        restaurant_name     TEXT
    );  '''
    cursor.execute(create_table_query)
    cursor.close()
    conn.close()
    print("Table 'survey' created")


def insert_form(name, frequency, age, meal_time, restaurant, restaurant_name):
    conn = get_db_connection()
    cursor = conn.cursor()
    insert_query = '''
    INSERT INTO survey (name, frequency, age, meal_time, restaurant, restaurant_name)
    VALUES (%s, %s, %s, %s, %s, %s);    '''
    cursor.execute(insert_query, (name, frequency, age, meal_time, restaurant, restaurant_name))
    cursor.close()
    conn.close()
    print("Data inserted")

def get_data(order = ""):
    conn = get_db_connection()
    cur = conn.cursor()
    if order =="reverse":
        cur.execute('SELECT * FROM survey ORDER BY survey_date DESC')
    else:
        cur.execute('SELECT * FROM survey survey_date')
    # cur.description has info of each column, starts at 0
    col_names = [desc[0] for desc in cur.description]

    # cur.fetchall() returns all rows in list
    # zip(col_names, row) pairs(zips) each col name with respective row values
    # dict converts the pairs into dictionary key, value pairs (col, row pairs)
    surveys = [dict(zip(col_names, row)) for row in cur.fetchall()]
    cur.close()
    conn.close()
    return surveys


# give list of tuples, and split tuples in key, value dictionary
# do this so data is better read by jinja2 template
def make_dictionary(data):
    key = [key for key, _ in data]
    value = [value for _, value in data]
    return {'labels': key, 'data': value}



def chart_get_age():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT age, COUNT(*) as count FROM survey GROUP BY age ORDER BY age;")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return make_dictionary(data)


def chart_get_meal_time():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT meal_time, COUNT(*) as count FROM survey GROUP BY meal_time ORDER BY meal_time;")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return make_dictionary(data)


def chart_get_frequency():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT frequency, COUNT(*) as count FROM survey GROUP BY frequency ORDER BY frequency;")
    data = cursor.fetchall()
    cursor.close()
    conn.close()
    return make_dictionary(data)


def chart_get_responses_per_day():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT DATE(survey_date) as survey_day, COUNT(*) as count FROM survey GROUP BY survey_day ORDER BY survey_day;")

    data = cursor.fetchall()
    formatted_data = [(d.strftime('%Y-%m-%d'), count) for d, count in data]

    cursor.close()
    conn.close()
    return make_dictionary(formatted_data)

def get_text_responses():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT restaurant_name FROM survey WHERE restaurant_name != '';")
    responses = cursor.fetchall()
    cursor.close()
    conn.close()
    return [response[0] for response in responses]


# print(chart_get_age())
# print(chart_get_meal_time())
# print(chart_get_frequency())

# print(make_dictionary(chart_get_meal_time()))



if __name__ == "__main__":
    create_table()  # Tmake sure table exists
    # insert_form('John Doe', '2 times', '25', 'Dinner', True, 'Chipotle')