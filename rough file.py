import sqlite3 as sq
conn = sq.connect(database='phone_log.db')
c = conn.cursor()
c.execute("SELECT name FROM sqlite_master WHERE type='table';")

print(c.fetchall())
conn.close()

# CREATE TABLE user_data(VAL_NO, USER_NAME, NAME, PASSWORD, sq1, ans1, sq2, ans2)
# SELECT sq1, ans2 from user_data where USER_NAME = "gagan"
# SELECT USER_NAME from user_data
# DROP TABLE user_data
# SELECT * from user_data
# c.execute('SELECT * FROM me_ADMIN')
# c.execute("SELECT name FROM sqlite_master WHERE type='table';")