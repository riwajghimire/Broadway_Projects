import sqlite3
import csv
COLUMNS = (
         'first_name',
         'last_name',
         'company_name',
         'address',
         'city',
         'county',
         'state',
         'zip',
         'phone1',
         'phone2',
         'email',
         'web'
        )

def create_connection():
    try:
        con = sqlite3.connect("users.sqlite3")
        return con
    except Exception as e:
        print("ERROR: ", e)


INPUT_STRING = """
Enter The Option:
1. CREATE TABLE
2. DUMP users from csv INTO users TABLE
3. ADD new user INTO users TABLE
4. QUERY all users from TABLE
5. QUERY user from id from TABLE
6. QUERY specified no. of records from TABLE
7. DELETE all users
8. DELETE users by id
9. UPDATE user
10. Press any key to EXIT
"""


def create_table(con):
    CREATE_USERS_TABLE_QUERY = """
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        first_name CHAR(255) NOT NULL,
        last_name CHAR(255) NOT NULL,
        company_name CHAR(255) NOT NULL,
        address CHAR(255) NOT NULL,
        city CHAR(255) NOT NULL,
        county CHAR(255) NOT NULL,
        state CHAR(255) NOT NULL,
        zip REAL NOT NULL,
        phone1 CHAR(255) NOT NULL,
        phone2 CHAR(255) NOT NULL,
        email CHAR(255) NOT NULL,
        web TEXT
    );
    """
    cur = con.cursor()
    cur.execute(CREATE_USERS_TABLE_QUERY)
    print("User table was created successfully")


def read_csv():
    users = []
    with open("sample_users.csv", "r") as f:
        data = csv.reader(f)
        for user in data:
            users.append(tuple(user))

    return users[1:]  # Skip the header row


def insert_users(con, users):
    user_add_query = """
        INSERT INTO users
        (
         first_name,
         last_name,
         company_name,
         address,
         city,
         county,
         state,
         zip,
         phone1,
         phone2,
         email,
         web
        )
        VALUES(?,?,?,?,?,?,?,?,?,?,?,?);
    """
    cur = con.cursor()
    cur.executemany(user_add_query, users)  # Insert multiple rows
    con.commit()
    print(f"{len(users)} users were imported successfully")


def select_all_users(con):
    cur = con.cursor()
    users = cur.execute("SELECT * FROM users")
    for user in users:
        print(user)


def select_user_by_id(con, user_id):
    cur = con.cursor()
    users = cur.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    for user in users:
        print(user)


def select_specified_no_of_users(con, no_of_users):
    cur = con.cursor()
    users = cur.execute("SELECT * FROM users LIMIT ?;", (no_of_users,))
    for user in users:
        print(user)


def delete_users(con):
    cur = con.cursor()
    cur.execute("DELETE FROM users;")
    con.commit()
    print("ALL users were deleted")

def delete_user_by_id(con, user_id):
    cur = con.cursor()
    cur.execute("DELETE FROM users WHERE id = ?;", (user_id,))
    con.commit()
    print("USER was deleted successfully")



def update_user_by_id(con,user_id,column_name,column_value):
    cur = con.cursor()
    cur.execute(
        f"UPDATE users set {column_name}=? where id=?;",(column_value,user_id)
        )
    con.commit()
    print(
        f"[{column_name} was updated with value [{column_value}] of user with id [{user_id}]"
    )

def main():
    con = create_connection()
    while True:
        user_input = input(INPUT_STRING)

        if user_input == "1":
            create_table(con)
        elif user_input == "2":
            users = read_csv()
            insert_users(con, users)
        elif user_input == "4":
            select_all_users(con)
        elif user_input == "5":
            user_id = input("ENTER USER ID: ")
            if user_id.isdigit():
                select_user_by_id(con, user_id)
            else:
                print("Invalid user ID")
        elif user_input == "6":
            no_of_users = input("ENTER the number of RECORDS: ")
            if no_of_users.isdigit():
                select_specified_no_of_users(con, int(no_of_users))
            else:
                print("INVALID number")
        elif user_input == "7":
            confirmation = input("ARE you sure you want to DELETE ALL USERS? (Y/N): ")
            if confirmation.lower() == "y":
                delete_users(con)
            else:
                print("DELETION CANCELLED")
        elif user_input == "8":
            user_id = input("Enter user id: ")
            if user_id.isdigit():
                delete_user_by_id(con, user_id)
            else:
                print("INVALID ID")
        
            
        elif user_input == "3":  
            user_data = []
            for column in COLUMNS:
                column_value = input(f"Enter the value for {column}: ")
                user_data.append(column_value)
            
            insert_users(con, [tuple(user_data)])
        
        elif user_input == "9" :
            user_id = input("enetr id of user:")
            if user_id.isnumeric():
                column_name= input(
                    f"Enter the column you want to edit please make sure its within {COLUMNS} : "
                )
                if column_name in COLUMNS:
                    column_values =input(f"enter the value for {column_name}")
                    update_user_by_id(con,user_id,column_name,column_value)
                else:
                    print("enter valid id")
        else:
            exit()  
    

                           




main()
