import mysql.connector as connector
class dbconnect:

    def main_connection(self):
        mydatabase = connector.connect(
                host="localhost",
                user="root",
                password="",
                database="atm"  
            )
        cur = mydatabase.cursor()
        return cur, mydatabase
    
def test_connection():
    print("hello world")


if __name__ == "__main__":
    test_connection()
    print("hELLO IT'S MEEE!", str.__dict__)
    pass
 