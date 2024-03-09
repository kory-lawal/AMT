from conn import dbconnect as mysql
import bcrypt
from getpass import getpass
import random
import os


class User:
    def __init__(self):
        self.cursor, self.mydatabase = mysql().main_connection()

    def welcome(self):
        try:
            option = int(input("Welcome to our ATM machine!\n1. Login\n2. Sign up\n3. Forgot Password\nChoose an option: "))
            if option == 1:
                self.login()
            elif option == 2:
                self.register() 
            elif option == 3:
                self.retrieve_password()
            else:
                print('Invalid choice. Please select 1, 2, or 3.')
                self.welcome()
        except ValueError:
            print('Invalid input. Please enter 1, 2, or 3.')
            self.welcome()

    def login(self):
        print("Logging In")
        name = input("Full Name: ")
        password = getpass("Password: ")

        query = 'SELECT password, accountnumber, balance FROM users WHERE name = %s'
        values = (name,)
        self.cursor.execute(query, values)

        results = self.cursor.fetchall()

        if results:
            stored_hashed_password = results[0][0]
            accountnumber = results[0][1]
            balance = results[0][2]

            if bcrypt.checkpw(password.encode('utf-8'), stored_hashed_password.encode('utf-8')):
                print("Login successful!")
                os.system('cls')
                print(f"Welcome back, {name}")
                print(f"Account Number: {accountnumber}")
                print(f"Current Balance: ${balance:.2f}")
                self.manage_balance(name, balance)
            else:
                print("Login failed. Passwords do not match.")
        else:
            print("Login failed. User not found. Please try again or register.")

    def manage_balance(self, name, balance):
        option = int(input("1. Deposit\n2. Withdraw\n3. Check Balance\n4. Logout\nChoose an option: "))
        if option == 1:
            amount = float(input("Enter the deposit amount: $"))
            new_balance = balance + amount
            self.update_balance(name, new_balance)
        elif option == 2:
            amount = float(input("Enter the withdrawal amount: $"))
            if amount <= balance:
                new_balance = balance - amount
                self.update_balance(name, new_balance)
            else:
                print("Insufficient funds.")
        elif option == 3:
            print(f"Current Balance: ${balance:.2f}")
            self.manage_balance(name, balance)  
        elif option == 4:
            print("Logging out.")
            self.welcome()
        else:
            print("Invalid option.")
            self.manage_balance(name, balance)

    def update_balance(self, name, new_balance):
        query = 'UPDATE users SET balance = %s WHERE name = %s'
        values = (new_balance, name)
        self.cursor.execute(query, values)
        self.mydatabase.commit()
        print("Transaction complete.")
        self.manage_balance(name, new_balance)
    
    def register(self):
        print("Creating A New Account")
        name = input("Full Name: ")
        email = input("Email: ")
        password = getpass("Password: ")
        confirm_password = getpass("Confirm Password: ")

        if password == confirm_password:
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            # Generate a 10-digit account number
            accountnumber = str(random.randint(10**9, 10**10 - 1))
            
            # Set an initial balance (you can change this as needed)
            initial_balance = 1000.0

            query = 'INSERT INTO users (name, email, password, accountnumber, balance) VALUES (%s, %s, %s, %s, %s)'
            user_details = (name, email, hashed_password, accountnumber, initial_balance)
            self.cursor.execute(query, user_details)

            self.mydatabase.commit()
            os.system('cls')
            print(f"Registration successful! Here is your account number: {accountnumber}")
            print(f"Initial Balance: ${initial_balance:.2f}")
            self.manage_balance(name, initial_balance)
        else:
            print("Passwords do not match. Please try again.")
    

    def retrieve_password(self):
        print("Password Retrieval")
        name = input("Full Name: ")
        email = input("Email: ")

        query = 'SELECT password FROM users WHERE name = %s AND email = %s'
        values = (name, email)
        self.cursor.execute(query, values)

        results = self.cursor.fetchall()

        if results:
            stored_hashed_password = results[0][0]
            plain_password = bcrypt.hashpw(stored_hashed_password.encode('utf-8'), bcrypt.gensalt())
            print("Retrieved password:", plain_password.decode('utf-8'))
        else:
            print("User not found. Please check your Full Name and Email and try again.")
        os.system('cls')
        
if __name__ == "__main__":
    user_instance = User()
    user_instance.welcome()
