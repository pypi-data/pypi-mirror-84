import sqlite3
import bcrypt

''' Instantiate database '''
conn = sqlite3.connect('users.db') # Setting up the database (and where)
c = conn.cursor() # This allows us to run commands to database

''' Create table '''
c.execute("""CREATE TABLE users (
 			username text,
 			password text,
 			display_name text,
 			friend1 text,
 			friend2 text,
 			friend3 text,
 			friend4 text,
 			friend5 text
 			)""")

''' Create test entries '''
thutch97_password = 'myPass'.encode('utf-8')
thutch97_password = bcrypt.hashpw(thutch97_password, bcrypt.gensalt())

rabbit_password = '123'.encode('utf-8')
rabbit_password = bcrypt.hashpw(rabbit_password, bcrypt.gensalt())

testuser1_password = 'testusr1'.encode('utf-8')
testuser1_password = bcrypt.hashpw(testuser1_password, bcrypt.gensalt())

testuser2_password = 'testusr2'.encode('utf-8')
testuser2_password = bcrypt.hashpw(testuser2_password, bcrypt.gensalt())

testuser3_password = 'testusr3'.encode('utf-8')
testuser3_password = bcrypt.hashpw(testuser3_password, bcrypt.gensalt())

with conn:
	c.execute("INSERT INTO users VALUES('thutch97',?,'Tom','rabbit','testuser1','testuser2','testuser3', 'None')", (thutch97_password,))
	c.execute("INSERT INTO users VALUES('rabbit',?,'Peter','thutch97','None','None','None','None')", (rabbit_password,))
	c.execute("INSERT INTO users VALUES('testuser1',?,'testo','thutch97','testuser2','testuser3','None', 'None')", (testuser1_password,))
	c.execute("INSERT INTO users VALUES('testuser2',?,'testinho','thutch97','testuser1','testuser3','None', 'None')", (testuser2_password,))
	c.execute("INSERT INTO users VALUES('testuser3',?,'testy','thutch97','testuser1','testuser2','None', 'None')", (testuser3_password,))

conn.close()