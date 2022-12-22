from cryptography.fernet import Fernet
from prettytable import PrettyTable
from dotenv import load_dotenv
from getpass import getpass

import sqlite3
import os
import time

load_dotenv(".env")

conn = sqlite3.connect("PasswordManager.db")
cur = conn.cursor()

def create_database():
    cur.execute("CREATE TABLE IF NOT EXISTS passwords (service VARCHAR, user VARCHAR, password VARCHAR)")

def clear_terminal():
    os.system('cls' if os.name == 'nt' else 'clear')


def DB_Query():
    clear_terminal()
    
    cur.execute("SELECT service, user FROM passwords")
    encrypted_data = cur.fetchall()

    decrypted_data = []
    for service, user in encrypted_data:
        decrypted_service = fernet.decrypt(service).decode('utf8')
        decrypted_user = fernet.decrypt(user).decode('utf8')
        decrypted_data.append([decrypted_service, decrypted_user])

    query = PrettyTable()
    query.clear_rows()
    query.field_names = ["Service", "User"]
    query.add_rows(
        decrypted_data
    )
    
    print(query)

def add():
    service = fernet.encrypt(bytes(input("Platform: ").title().encode('utf8')))
    user = fernet.encrypt(bytes(input("User: ").encode('utf8')))
    pw = fernet.encrypt(bytes(getpass("Password: ").encode('utf8')))

    cur.execute("INSERT INTO passwords (service, user, password) VALUES (?, ?, ?)", (service, user, pw))

    conn.commit()

def remove():
    del_service = input("Service you wish to delete: ").title()
    del_user = input("User you wish to delete: ")
    cur.execute("SELECT service, user FROM passwords")
    encrypted_data = cur.fetchall()
    for service, user in encrypted_data:
        decrypted_service = fernet.decrypt(service).decode('utf8')
        decrypted_user = fernet.decrypt(user).decode('utf8')
        if decrypted_service == del_service and decrypted_user == del_user:
            cur.execute("DELETE FROM passwords WHERE service=? and user=?", (service, user))
    conn.commit()

def get():
    get_service = input("Password Service: ").title()
    get_user = input("Password User: ")

    cur.execute("SELECT * FROM passwords")
    encrypted_data = cur.fetchall()
    for service, user, pwd in encrypted_data:
        decrypted_service = fernet.decrypt(service).decode('utf8')
        decrypted_user = fernet.decrypt(user).decode('utf8')
        if decrypted_service == get_service and decrypted_user == get_user:
            
            decrypted_pwd = fernet.decrypt(pwd).decode('utf8')
            info = PrettyTable()
            info.clear_rows()
            info.field_names = ["Service", "User", "Password"]
            info.add_row([decrypted_service, decrypted_user, decrypted_pwd])

            print(f"\n{info}")
    resume = input("Press ENTER to continue.").lower()

def update():
    update_service = input("Service you wish to update: ").title()
    update_user = input("User you wish to update: ")

    cur.execute("SELECT * FROM passwords")
    encrypted_data = cur.fetchall()
    for service, user, pwd in encrypted_data:
        decrypted_service = fernet.decrypt(service).decode('utf8')
        decrypted_user = fernet.decrypt(user).decode('utf8')
        if decrypted_service == update_service and decrypted_user == update_user:
            edit_service = fernet.encrypt(bytes(input("\nUpdate Service: ").title().encode('utf8')))
            edit_user = fernet.encrypt(bytes(input("Update User: ").encode('utf8')))
            edit_pwd = fernet.encrypt(bytes(getpass("Update Password: ").encode('utf8')))
            
            cur.execute("DELETE FROM passwords WHERE service=? and user=?", (service, user))
            cur.execute("INSERT INTO passwords (service, user, password) VALUES (?, ?, ?)", (edit_service, edit_user, edit_pwd))

    conn.commit()


create_database()
key = Fernet.generate_key()

if "FERNET_KEY" not in os.environ:
    with open(".env", "a") as f:
        f.write("FERNET_KEY=" + key.decode())

if "MASTER_PASSWORD" not in os.environ:
    while True:
        create_master_pw = input("Create a Master Password: ")
        confirm_master_pw = input("Confirm Master Password: ")
        if create_master_pw == confirm_master_pw:
            with open(".env", "a") as f:
                f.write("\nMASTER_PASSWORD=" + f'"{create_master_pw}"')
                break
        else:
            clear_terminal()

clear_terminal()
master_pw = getpass("Master Password: ")
if master_pw != os.getenv("MASTER_PASSWORD"):
    print("Incorrect Password. Shutting down...")
    time.sleep(5)
    quit(1)

load_dotenv(".env")

fernet = Fernet(os.getenv("FERNET_KEY"))
DB_Query()

while True:
    DB_Query()
    choice = input("Enter Choice (add/remove/get/update/quit): ").lower()

    if choice == 'add':
        add()
    elif choice == 'remove':
        remove()
    elif choice == 'get':
        get()
    elif choice == 'update':
        update()
    elif choice == 'quit':
        print("Shutting down...")
        time.sleep(3)
        break
    else:
        print("Invalid command.")
        time.sleep(3)

conn.commit()
conn.close()
