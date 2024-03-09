import mysql.connector

class Transaction:
    def __init__(self):
        self.mydatabase = mysql.connector.connect(
            host="localhost",
            user="root",
            password="",
            database="atm"  
        )
        self.cursor = self.mydatabase.cursor()

    def create_transaction(self, sender_account, receiver_account, amount):
        query = 'INSERT INTO transactions (sender_account_number, receiver_account_number, amount) VALUES (%s, %s, %s)'
        values = (sender_account, receiver_account, amount)
        self.cursor.execute(query, values)
        self.mydatabase.commit()

    def update_balances(self, sender_account, receiver_account, amount):
        # Update sender's balance (subtract the transaction amount)
        query = 'UPDATE users SET balance = balance - %s WHERE accountnumber = %s'
        values = (amount, sender_account)
        self.cursor.execute(query, values)
        
        # Update receiver's balance (add the transaction amount)
        query = 'UPDATE users SET balance = balance + %s WHERE accountnumber = %s'
        values = (amount, receiver_account)
        self.cursor.execute(query, values)

        self.mydatabase.commit()

    # def retrieve_transactions(self, account_number):
    #     query = 'SELECT sender_account_number, receiver_account_number, amount FROM transactions WHERE sender_account_number = %s OR receiver_account_number = %s'
    #     values = (account_number, account_number)
    #     self.cursor.execute(query, values)
    #     return self.cursor.fetchall()
    
