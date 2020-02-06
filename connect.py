import sqlite3
import queries

db = sqlite3.connect("test.db")
db.isolation_level = None

c = db.cursor()

# c.executescript(queries.INIT_DB)
# c.executescript(queries.SET_TEST_VALUES)

c.execute("SELECT koodi, nimi FROM Paketti, Asiakas as A WHERE asiakas_id = A.id;")
print(c.fetchall())
