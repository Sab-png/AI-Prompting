# fonte
# https://towardsdatascience.com/an-easy-beginners-guide-to-sqlite-in-python-and-pandas-fbf1f38f6800

import sqlite3 as db
import pandas as pd


# DB SETUP

conn = db.connect('my_database.db')

c = conn.cursor()

c.execute("SELECT name FROM sqlite_master WHERE type='table';")
print(c.fetchall())

c.execute("INSERT INTO employees VALUES (12986,'Michael','Scott')")
c.execute("INSERT INTO employees VALUES (12987,'Dwight','Schrute')")


new_employees = [(12987, 'Jim', 'Halpert'),
 (12988, 'Pam', 'Beesly'),
 (12989, 'Andy', 'Bernard'),
 (12990, 'Kevin', 'Malone'),
 (12991, 'Toby', 'Flenderson'),
 (12992, 'Angela', 'Martin'),
 (12993, 'Stanley', 'Hudson')]
c.executemany('INSERT INTO employees VALUES (?, ?, ?)', new_employees)


conn.commit()



# PANDAS

df_employees = pd.read_sql_query('select * from employees', conn)



conn.commit()
c.close()
conn.close()
