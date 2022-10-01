# Current Features:
# - Add more
# - Check if correct
# - View Previous (including password when select a platform)

# Started with pulling passwords

import sqlite3
from getpass import getpass

def add_info(add_platform, add_email, add_password):
    cur.execute("INSERT INTO accounts(platform, email, password) VALUES(?, ?, ?)", (add_platform, add_email, add_password))
    conn.commit()


def specific(picked_platform):
    res = cur.execute("SELECT * FROM accounts WHERE platform=?", [picked_platform])
    rows = res.fetchall
    for row in rows:
        print(row)


def view_previous():
    res = cur.execute("SELECT platform FROM accounts")
    rows = res.fetchall()
    for row in rows:
        print(row)


conn = sqlite3.connect("PasswordManager.db")
cur = conn.cursor()
cur.execute("CREATE TABLE IF NOT EXIST accounts(platform, email, password)")

print("All information provided will be protected.")

create_password = input("Wish to add new account? (Y/N)\n> ").lower()

while True:
    if create_password == 'y':
        platform = input("\nPlatform: ")
        email = input("Email: ")
        password = getpass("Password: ")
        add_info(platform, email, password)
    elif create_password == 'n':
        see_previous = input("Do you wish to see previous passwords? (Y/N)\n> ").lower()
        if see_previous == 'y':
            view_previous()
            pull_password = input("Do you wish to view a password? (Y/N)\n> ").lower()
            if pull_password == 'y':
                what_platform = input("what platform?\n> ").title()
                specific(what_platform)

        elif see_previous == 'n':
            break
    add_more = input("Do you wish to add more? (Y/N)\n> ")
    if add_more == 'y':
        create_password = add_more
    elif add_more == 'n':
        break
    else:
        print("Assuming no.")
        break

conn.close()