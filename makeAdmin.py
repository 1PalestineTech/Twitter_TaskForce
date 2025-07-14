from werkzeug.security import  generate_password_hash
import sqlite3


username = input("Enter username: ").trim()
password = generate_password_hash(input("Enter Password: ").trim())
database = sqlite3.connect('database.db')
database.execute(
    """
    INSERT INTO ADMINS (username,password) 
    VALUES (?,?);""",(username,password))
database.commit()
database.close()