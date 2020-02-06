import sqlite3

db = sqlite3.connect("testi.db")
db.isolation_level = None

c = db.cursor()

c.execute("DROP TABLE IF EXISTS Tuotteet")
c.execute("CREATE TABLE Tuotteet (id INTEGER PRIMARY KEY, nimi TEXT, hinta INTEGER)")
c.execute("INSERT INTO Tuotteet (nimi,hinta) VALUES ('retiisi',7)")
c.execute("INSERT INTO Tuotteet (nimi,hinta) VALUES ('porkkana',5)")
c.execute("INSERT INTO Tuotteet (nimi,hinta) VALUES ('nauris',4)")
c.execute("INSERT INTO Tuotteet (nimi,hinta) VALUES ('lanttu',8)")
c.execute("INSERT INTO Tuotteet (nimi,hinta) VALUES ('selleri',4)")

c.execute("SELECT * FROM Tuotteet")
print(c.fetchall())

# c = db.cursor()

# print("Anna tuotteen nimi:")
# nimi = input()

# c.execute("SELECT hinta FROM Tuotteet WHERE nimi=?",[nimi]) # parametrisointi
# tiedot = c.fetchone() # hae 1 tai Nil
# if tiedot != None:
#     print("Hinta:",tiedot[0])
# else:
#     print("Tuotetta ei löytynyt")    
