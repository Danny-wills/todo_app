import psycopg2
import psycopg2.extras
from flask import Flask, render_template, request, redirect, url_for, flash, session
import re
from werkzeug.security import generate_password_hash, check_password_hash
from secrets_manager import get_secret

secrets = get_secret()

conn = psycopg2.connect(
    database=secrets['database'],
    host=secrets['host'],
    user=secrets['user'],
    password=secrets['password'],
    port=secrets['port']
)

cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)


select_script = "SELECT * FROM todos"
select_script_w_filter = "SELECT * FROM todos WHERE todo = %s"
delete_script = 'DELETE FROM todos WHERE id = %s AND user_id = %s'
exit_message = "Exiting now"

app = Flask(__name__)
# with open('secret_key.txt', 'r') as secret_key:
#     app.secret_key = secret_key.read()
app.secret_key = secrets['app.secret']

@app.route('/')
def index():
    # Check if user is logged in 
    if 'loggedin' in session:
        username = session['username']
        name = session['name']
        # Retrieve user ID based on the username
        cursor.execute('SELECT id FROM users WHERE username = %s', (username,))
        user_id = cursor.fetchone()[0]
        # Fetch todos for the user based on user_id
        cursor.execute('SELECT * FROM todos WHERE user_id = %s', (user_id,))
        todos = cursor.fetchall()
        conn.commit()
        # user is logged in show them homepage
        return render_template('index.html', todos=todos, username=username, name=name)
    # user is not logged in redirect to login page
    return redirect(url_for('login'))

@app.route('/login/', methods=['GET', 'POST'])
def login():
    # Check if usernsme and password POST requests exist
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form:
        username     = request.form['username']
        password     = request.form['password']

        # check if account exists
        cursor.execute('SELECT * FROM users WHERE username = %s', (username,))
        account = cursor.fetchone()

        if account:
            password_rs = account['password']
            # if account exists in users table in our database
            if check_password_hash(password_rs, password):
                # Create session data
                session['loggedin'] = True
                session['id'] = account['id']
                session['username'] = account['username']
                session['name'] = account['name']
                # Redirect to home page
                return redirect(url_for('index'))  
            else:
                flash('Incorrect username/password')
        else:
            flash('Account does not exist')
    return render_template('login.html')

@app.route('/logout')
def logout():
    # Remove session data, log the user out
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    session.pop('name', None)
    # Redirect to login page
    return redirect(url_for('login'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    # check if username, password and email POST request exists (user submitted form)
    if request.method == 'POST' and 'username' in request.form and 'password' in request.form and 'email' in request.form:
        name         = request.form['name']
        cap_name     = name.capitalize()
        email        = request.form['email']
        username     = request.form['username']
        password     = request.form['password']

        hashed_password = generate_password_hash(password)

        # Check if account exists in database
        cursor.execute('SELECT * FROM users where username = %s', (username,))
        account = cursor.fetchone()
        # If account exits show error
        if account:
            flash("Account already exists")
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            flash('Invalid email address!')
        elif not re.match(r'[A-Za-z0-9]+', username):
            flash('Username must contain only characters and numbers!')
        elif not username or not password or not email:
            flash('Please fill out the form!')
        else:
            # Account doesn't exist and the form data is valid, insert new accoun t into users table
            cursor.execute("INSERT INTO users (name, username, password, email) VALUES (%s,%s,%s,%s)", (cap_name, username, hashed_password, email))
            conn.commit()
            return redirect(url_for('index'))
    elif request.method == 'POST':
        # Form is empty...(no POST data)
        flash('Please fill out the form!')            
    return render_template('register.html')

@app.route('/add', methods=['POST'])
def add_todo():
    # Get user todo input
    todo    = request.form.get('add-todo')
    # Get user id from session
    user_id = session['id']
    if not todo:
        flash("Please enter a todo!")
    else:
        cap_todo = todo.capitalize()
        cursor.execute("INSERT INTO todos (todo, user_id) VALUES (%s, %s)", (cap_todo, user_id))
        conn.commit()
    return redirect(url_for('index'))


@app.route('/delete/<int:id>')
def del_todo(id):
    user_id = session['id']
    cursor.execute(delete_script, (id, user_id))
    conn.commit()
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=False)






