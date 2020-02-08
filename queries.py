INIT_DB =           """ DROP TABLE IF EXISTS Asiakas;
                        DROP TABLE IF EXISTS Paikka;
                        DROP TABLE IF EXISTS Paketti;
                        DROP TABLE IF EXISTS Tapahtuma;
                        PRAGMA foreign_keys = ON;
                        CREATE TABLE Asiakas (
                          nimi TEXT PRIMARY KEY
                        );
                        CREATE TABLE Paikka (
                          nimi TEXT PRIMARY KEY
                        );
                        CREATE TABLE Paketti (
                          koodi VARCHAR(200) PRIMARY KEY,
                          asiakas_nimi TEXT,
                          FOREIGN KEY(asiakas_nimi) REFERENCES Asiakas(nimi)
                        );
                        CREATE TABLE Tapahtuma (
                          id INTEGER PRIMARY KEY,
                          paketti_koodi VARCHAR(200),
                          ajankohta TEXT NOT NULL,
                          paikka_nimi TEXT,
                          kuvaus TEXT,
                          FOREIGN KEY(paketti_koodi) REFERENCES Paketti(koodi),
                          FOREIGN KEY(paikka_nimi) REFERENCES Paikka(nimi)
                        ); """

ADD_LOCATION =      """INSERT INTO Paikka(nimi) VALUES (?);"""
ADD_CUSTOMER =      """INSERT INTO Asiakas(nimi) VALUES (?);"""
ADD_PARCEL =        """INSERT INTO Paketti(koodi, asiakas_nimi) VALUES (?,?);"""
ADD_EVENT =         """INSERT INTO Tapahtuma(paketti_koodi, paikka_nimi, kuvaus, ajankohta) VALUES (?,?,?,datetime('now', 'localtime'));"""
GET_EVENTS_FOR_PARCEL = """SELECT ajankohta, paikka_nimi, kuvaus FROM Tapahtuma WHERE paketti_koodi=?;"""
GET_PARCELS_FOR_CUSTOMER = """SELECT koodi, (SELECT count(*) FROM Tapahtuma WHERE paketti_koodi = P.koodi) FROM Paketti P WHERE asiakas_nimi LIKE ?;"""

PAIKAT =            """SELECT * FROM Paikka;"""
ASIAKKAAT =         """SELECT * FROM Asiakas;"""
PAKETIT =           """SELECT * FROM Paketti;"""
TAPAHTUMAT =        """SELECT * FROM Tapahtuma;"""

SET_TEST_VALUES = """ INSERT INTO Asiakas(nimi) VALUES ('Kiipeli'), ('Juukeli'), ('Peepeli'), ('Aapeli');
                      INSERT INTO Paikka(nimi) VALUES ('Kouvola'), ('Kotka'), ('Hamina'), ('Pyhtää');
                      INSERT INTO Paketti(koodi, asiakas_id) VALUES ('A0001', 1), ('B0002', 1), ('C0003', 3), ('D0004', 4);
                      INSERT INTO Tapahtuma(kuvaus, ajankohta, paketti_koodi, paikka_id)
                      VALUES
                        ('leimaus', datetime('now', 'localtime'), 'A0001', 1),
                        ('leimaus', datetime('now', 'localtime'), 'B0002', 1),
                        ('leimaus', datetime('now', 'localtime'), 'C0003', 3),
                        ('leimaus', datetime('now', 'localtime'), 'D0004', 2);
                  """