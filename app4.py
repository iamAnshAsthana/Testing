import mysql.connector

connection = mysql.connector.connect(
    host = '127.0.0.1',
    user = 'root', 
    password="@ansh.0603", 
    database = 'python_batch'
)
cursor = connection.cursor(dictionary=True)

user_choice = {
    1: 'INSERT',
    2: 'UPDATE',
    3: 'DELETE',
    4: 'SELECT'
}

ask_user_choice = f"""
Please select your choice
Press 1 for Insert
Press 2 for Update
Press 3 for Delete
Press 4 for Select
"""

while True:
    user_select_choice = input(ask_user_choice)
    realvalid_choice = user_choice.get(int(user_select_choice))
    if realvalid_choice:
        if realvalid_choice == 'INSERT':
            while True:
                name = input('Enter name to insert: ')
                if len(name) >= 5 and len(name) <= 20:
                    break
                else:
                    print("Please enter a valid name with Min 5 and Max 10 and all char should be Alpha")
            while True:
                email = input('Enter email to insert: ')
                if len(email) >= 13 and len(email) <= 20 and email.endswith("@gmail.com"):
                    break
                else:
                    print("You entered invalid email address")
            while True:
                mobile = input('Enter mobile to insert: ')
                if len(mobile) == 10 and mobile.isnumeric():
                    break
                else:
                    print("You entered an invalid number")
            query = "insert into user (name,email,mobile) values (%s,%s,%s)"
            cursor.execute(query,(name,email,mobile))
            connection.commit()
            print("Record inserted successfully")
        elif realvalid_choice == 'DELETE':
            while True:
                del_id = input("Enter id which you want to delete: ")
                if del_id.isnumeric() and int(del_id):
                    break
                print("Try Again, you entered an invalid id.")

            check_query = "SELECT id FROM user WHERE id = %s"
            cursor.execute(check_query, (del_id,))
            
            record_exists = cursor.fetchone() 
            
            if record_exists:
                delete_query = "DELETE FROM user WHERE id = %s"
                cursor.execute(delete_query, (del_id,))
                
                connection.commit()
                print("Record deleted successfully!")
            else:
                print("It's not in the table")
            break
        else:
            print('WIP')
    else:
        print('Please enter a valid no')