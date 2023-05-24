import psycopg2
import psycopg2.extras


conn = psycopg2.connect(
    database="todo_app",
    host="todo-app.cxrkzay6teds.us-east-1.rds.amazonaws.com",
    user="postgress",
    password="Owdanny400",
    port="5432"
)

cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
    id SERIAL PRIMARY KEY,
    name TEXT UNIQUE NOT NULL,
    username TEXT NOT NULL,
    email TEXT UNIQUE NOT NULL,
    password TEXT NOT NULL
    );""")

cursor.execute("""
    CREATE TABLE IF NOT EXISTS todos (
    id SERIAL PRIMARY KEY,
    todo TEXT,
    user_id INTEGER REFERENCES users(id)
    );
""")

conn.commit()




