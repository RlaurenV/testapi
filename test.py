import mysql.connector
from mysql.connector import errorcode

# Define the database connection parameters
config = {
    'host': 'matinacrossing.mysql.database.azure.com',
    'user': 'admindb',
    'password': '@Qwerty123',
    'database': 'brgy_informationdb',
    'client_flags': [mysql.connector.ClientFlag.SSL],
    'ssl_ca': r'C:\Users\User\Downloads\DigiCertGlobalRootCA.crt.pem',  # Do not specify SSL certificates
}

# construct connection string

try:
    conn = mysql.connector.connect(**config)
    print("connection established")
except mysql.connector.Error as err:
    if err.errno == errorcode.ER_ACCESS_DENIED_ERROR:
        print("something is wrong with the username or password")
    elif err.errno == errorcode.ER_BAD_DB_ERROR:
        print("database does not exist")
    else:print(err)
else:
    cursor = conn.cursor()

    # create table
    cursor.execute("CREATE TABLE test (id serial PRIMARY KEY, name VARCHAR(50), password VARCHAR(50));")
    print("Finished creating table")

    # insert data into the table
    cursor.execute("INSERT INTO test (name,password) VALUES (%s,%s);",("admin","password"))
    print("inserted", cursor.rowcount,"row(s) of data")

    #clean up
    conn.commit()
    cursor.close()
    conn.close
    print("Done")
    