import mysql.connector 

mydb = mysql.connector.connect(
    host = 'localhost',
    user = 'root',
    passwd = 'Emiza@1234'
    )

my_cursor = mydb.cursor()
my_cursor.execute("SHOW DATABASES ")
for db in my_cursor.fetchall():
    print(db)


