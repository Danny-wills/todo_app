import psycopg2
import psycopg2.extras

conn = psycopg2.connect(
    database="todo_app",
    host="localhost",
    user="postgres",
    password="Owdanny400",
    port="5432"
)

cursor = conn.cursor(cursor_factory=psycopg2.extras.DictCursor)

cursor.execute("""
    CREATE TABLE IF NOT EXISTS todos (
    todo TEXT PRIMARY KEY
    );
""")


insert_script = "INSERT INTO todos (todo) VALUES (%s)"
select_script = "SELECT * FROM todos"
select_script_w_filter = "SELECT * FROM todos WHERE todo = %s"
delete_script = 'DELETE FROM todos WHERE todo = %s'
exit_message = "Exiting now"

while True:
    try:
        menu = """
        Menu: 
        1. Enter a new todo
        2. List all todo
        3. Delete a todo
        4. Exit   
        """

        print(menu)
        choice = int(input("Chose an option between 1 to 4: "))

        if choice == 1:
            Menu = """
            New todo...enter exit when done
            """
            print(Menu)
            while True:
                newTodo = input("Enter new todo: ").capitalize()
                if newTodo == "Exit":
                    break
                else:
                    cursor.execute(insert_script, (newTodo,))
                    print(f"Todo ('{newTodo}') added\n")

        elif choice == 2:
            cursor.execute(select_script)
            rows = cursor.fetchall()
            while True:
                if rows:
                    print("\nHere's your todo list\n")
                    for row in rows:
                        print(row['todo'])
                    put = input("\nEnter exit when done: ").capitalize()
                    if put == "Exit":
                        break
                    else:
                        print("Please enter a valid response")
                else:           
                    print("\nNo todo, please add a todo to begin")
                    break
                
        elif choice == 3:
            # Retrieve all todos in table
            cursor.execute(select_script)
            # Check if table is empty
            if not cursor.fetchall():
                print("\nTODO LIST EMPTY!!!, PLEASE ADD TODO")
            else:
                deltodo = input("\nEnter a todo to delete: ").capitalize()
                cursor.execute(select_script_w_filter, (deltodo,))
                del_rows = cursor.fetchall()
                # Check if the todo to delete is in the list of todos
                if del_rows:
                    for row in del_rows:
                        sure = input(f"Are you sure to delete {row} (y/n): ").upper()
                        if sure == 'Y':
                            cursor.execute(delete_script, (deltodo,))
                            print(row["todo"], "deleted successfully")
                        elif sure == 'N':
                            continue
                        else:
                            print("Please enter either y or n")
                else:
                    print(f"{deltodo} is not in your todo list, please try again")       

        elif choice == 4:
            print(f"\n{exit_message}\n")
            break
        else:
            print("Invalid!!! Enter a number from the list (1 - 4)")
        conn.commit()
    except ValueError as e:
        print("Invalid!!!, please enter a valid integer.")
cursor.close()
conn.close()