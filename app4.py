import mysql.connector
from dotenv import load_dotenv
import os
load_dotenv()

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
RESET = '\033[0m'

connection = mysql.connector.connect(
    host = os.getenv("DB_HOST"),
    user = os.getenv("DB_USER"), 
    password=os.getenv("DB_PASSWORD"), 
    database = os.getenv("DB_DATABASE")
)
cursor = connection.cursor(dictionary=True)

user_choice = {
    1: 'INSERT',
    2: 'UPDATE',
    3: 'DELETE',
    4: 'SELECT'
}

ask_user_choice = f"""
{BLUE}
Please select your choice
Press 1 for Insert
Press 2 for Update
Press 3 for Delete
Press 4 for Select
{RESET}
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
                    print("{RED}Please enter a valid name with Min 5 and Max 10 and all char should be Alpha{RESET}")
            while True:
                email = input('Enter email to insert: ')
                if len(email) >= 13 and len(email) <= 20 and email.endswith("@gmail.com"):
                    break
                else:
                    print(f"{RED}Invalid email address, Email must have following things: end with @gmail.com min 13 char max 20 char{RED}")
            while True:
                mobile = input('Enter mobile to insert: ')
                if len(mobile) == 10 and mobile.isnumeric():
                    break
                else:
                    print(f"{RED}Invalid number{RESET}")
            query = "insert into user (name,email,mobile) values (%s,%s,%s)"
            cursor.execute(query,(name,email,mobile))
            connection.commit()
            print(f"{GREEN}Record inserted successfully{RESET}")
            continue
        elif realvalid_choice == 'DELETE':
            while True:
                del_id = input("Enter id which you want to delete: ")
                if del_id.isnumeric() and int(del_id):
                    break
                print(f"{RED}Try Again, you entered an invalid id.{RESET}")

            check_query = "SELECT id FROM user WHERE id = %s"
            cursor.execute(check_query, (del_id,))
            
            record_exists = cursor.fetchone() 
            
            if record_exists:
                delete_query = "DELETE FROM user WHERE id = %s"
                cursor.execute(delete_query, (del_id,))
                
                connection.commit()
                print(f"{GREEN}Record deleted successfully!{RESET}")
            else:
                print(f"{RED}It's not in the table{RESET}")
            continue
        elif realvalid_choice == 'SELECT':
            select = 0
            exit_select_option = False

            cursor.execute("SELECT COUNT(*) AS total_count FROM user")
            tot_rec = cursor.fetchone()['total_count']

            if tot_rec == 0:
                print(f"{YELLOW}Table is Empty.{RESET}")
                continue 
            while True:
                if exit_select_option:
                    break
                remaining = tot_rec - select
                if remaining <= 0:
                    while True:
                        u_choice = input(f"{BLUE}All data displayed. Do you want to return to the main menu?\n2. Main Menu\n{RESET}")
                        if u_choice == '2':
                            exit_select_option = True
                            break
                        print(f"{RED}Invalid Choice, Try Again with a valid number!{RESET}")
                    continue

                r_to_dis = 0
                while True:
                    choice = input(f"How many rows do you want to see: ")
                    if choice.isnumeric() and int(choice) > 0:
                        r_to_dis = int(choice)
                        if r_to_dis > remaining:
                            r_to_dis = remaining
                        break
                    print(f"{RED}Invalid input, Try Again with a valid input!{RESET}")
                query = "SELECT id, name, email, mobile FROM user ORDER BY id ASC LIMIT %s OFFSET %s"
                cursor.execute(query, (r_to_dis, select))
                records = cursor.fetchall()
                if not records:
                    print(f"{YELLOW}No records to display.{RESET}")

                for record in records:
                    print(f"ID:     {record.get('id', 'No record found')}")
                    print(f"Name:   {record.get('name', 'No record found')}")
                    print(f"Email:  {record.get('email', 'No record found')}")
                    print(f"Mobile: {record.get('mobile', 'No record found')}")
                select += len(records)
                remaining = tot_rec - select
                if remaining > 0:
                    while True:
                        choice_2 = input(f"{BLUE}Do you want to see more or return to the main menu?\n1. See more\n2. Main Menu\n{RESET}").strip()
                        if choice_2 == '1':
                            break
                        elif choice_2 == '2':
                            exit_select_option = True
                            break
                        print(f"{RED}Invalid choice. Enter 1 or 2.{RESET}")
                if exit_select_option or remaining <= 0:
                    continue
            continue
        elif realvalid_choice == 'UPDATE':
            cursor.execute("SELECT id, name, email, mobile FROM user ORDER BY id ASC")
            all_records = cursor.fetchall()
            
            for record in all_records:
                print(f"ID:  {record.get('id', 'No record found')}")
                print(f"Name:  {record.get('name', 'No record found')}")
                print(f"Email: {record.get('email', 'No record found')}")
                print(f"Mobile: {record.get('mobile', 'No record found')}")
                
            if not all_records:
                print(f"{YELLOW}Nothing's there to update.{RESET}")
                continue
                
            updation = None
            update_d = None
            
            while True:
                updated_details = input("Please give id which you want to Update: ")
                if updated_details.isnumeric() and int(updated_details) > 0:
                    update_d = int(updated_details)
                    check_query = "SELECT id, name, email, mobile FROM user WHERE id = %s"
                    cursor.execute(check_query, (update_d,))
                    updation = cursor.fetchone()

                    if updation:
                        break
                    print(f"{RED}ID not found in the table.{RESET}")
                else:
                    print(f"{RED}Try Again with a valid ID.{RESET}")
            
            print(f"{BLUE}Old Data{RESET}")
            print(f"ID:    {updation['id']}")
            print(f"Name:  {updation['name']}")
            print(f"Email: {updation['email']}")
            print(f"Mobile: {updation['mobile']}")
            
            def new_rec(p, c_val, v_type):
                while True:
                    u_i = input(p)
                    if not u_i:
                        return c_val

                    is_valid = False
                    message = ""
                    
                    if v_type == 'name':
                        if len(u_i) >= 5 and len(u_i) <= 20:
                            is_valid = True
                        else:
                            message = "Name must be between 5 and 20 characters."
                    
                    elif v_type == 'email':
                        if len(u_i) >= 13 and len(u_i) <= 20 and u_i.endswith("@gmail.com"):
                            is_valid = True
                        else:
                            message = "Email must end with @gmail.com and be 13-20 characters long."
                            
                    elif v_type == 'mobile':
                        if len(u_i) == 10 and u_i.isnumeric():
                            is_valid = True
                        else:
                            message = "Mobile number must be exactly 10 digits and numeric."
                            
                    if is_valid:
                        return u_i
                    else:
                        print(f"{RED}Invalid input: {message}{RESET}")

            
            new_n = new_rec(f"New Name: ", updation['name'], 'name')
            new_e = new_rec(f"New Email: ", updation['email'], 'email')
            new_m = new_rec(f"New Mobile: ", updation['mobile'], 'mobile')
            
            update_query = "UPDATE user SET name = %s, email = %s, mobile = %s WHERE id = %s"
            cursor.execute(update_query, (new_n, new_e, new_m, update_d))
            connection.commit()
              
            if (new_n != updation['name'] or new_e != updation['email'] or new_m != updation['mobile']):
                print(f"{GREEN}Record id updated successfully!{RESET}")
            else:
                print(f"{YELLOW}No changes made.{RESET}")
            continue
    else:
        print(f'{RED}Please enter a valid no{RESET}')