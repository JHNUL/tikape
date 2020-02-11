INIT_DB =                   """ PRAGMA foreign_keys = OFF;
                                DROP TABLE IF EXISTS Asiakkaat;
                                DROP TABLE IF EXISTS Paikat;
                                DROP TABLE IF EXISTS Paketit;
                                DROP TABLE IF EXISTS Tapahtumat;
                                PRAGMA foreign_keys = ON;
                                CREATE TABLE Asiakkaat (
                                  id INTEGER PRIMARY KEY,
                                  nimi TEXT NOT NULL UNIQUE
                                );
                                CREATE TABLE Paikat (
                                  id INTEGER PRIMARY KEY,
                                  nimi TEXT NOT NULL UNIQUE
                                );
                                CREATE TABLE Paketit (
                                  id INTEGER PRIMARY KEY,
                                  koodi VARCHAR(200) NOT NULL UNIQUE,
                                  asiakas_id INTEGER REFERENCES Asiakkaat(id)
                                );
                                CREATE TABLE Tapahtumat (
                                  paketti_id INTEGER REFERENCES Paketit(id),
                                  paikka_id INTEGER REFERENCES Paikat(id),
                                  ajankohta TEXT NOT NULL,
                                  kuvaus TEXT
                                );
                                """

INIT_DB_WITH_INDICES =      """ PRAGMA foreign_keys = OFF;
                                DROP TABLE IF EXISTS Asiakkaat;
                                DROP TABLE IF EXISTS Paikat;
                                DROP TABLE IF EXISTS Paketit;
                                DROP TABLE IF EXISTS Tapahtumat;
                                PRAGMA foreign_keys = ON;
                                CREATE TABLE Asiakkaat (
                                  id INTEGER PRIMARY KEY,
                                  nimi TEXT NOT NULL UNIQUE
                                );
                                CREATE TABLE Paikat (
                                  id INTEGER PRIMARY KEY,
                                  nimi TEXT NOT NULL UNIQUE
                                );
                                CREATE TABLE Paketit (
                                  id INTEGER PRIMARY KEY,
                                  koodi VARCHAR(200) NOT NULL UNIQUE,
                                  asiakas_id INTEGER REFERENCES Asiakkaat(id)
                                );
                                CREATE TABLE Tapahtumat (
                                  paketti_id INTEGER REFERENCES Paketit(id),
                                  paikka_id INTEGER REFERENCES Paikat(id),
                                  ajankohta TEXT NOT NULL,
                                  kuvaus TEXT
                                );
                                CREATE INDEX idx_asiakas_nimi ON Asiakkaat (nimi);
                                CREATE INDEX idx_paikka_nimi ON Paikat (nimi);
                                CREATE INDEX idx_paketti_id ON Tapahtumat (paketti_id);
                                CREATE INDEX idx_paikka_id ON Tapahtumat (paikka_id);
                                CREATE INDEX idx_asiakas_id ON Paketit (asiakas_id);
                                CREATE INDEX idx_koodi ON Paketit (koodi);
                                """

BEGIN_TRANSACTION =         """BEGIN TRANSACTION;"""
COMMIT =                    """COMMIT;"""

GET_CUSTOMER_ID =           """SELECT id FROM Asiakkaat WHERE nimi = ?;"""
GET_PARCEL_ID =             """SELECT id FROM Paketit WHERE koodi = ?;"""
GET_LOCATION_ID =           """SELECT id FROM Paikat WHERE nimi = ?;"""

ADD_LOCATION =              """INSERT INTO Paikat(nimi) VALUES (?);"""
ADD_CUSTOMER =              """INSERT INTO Asiakkaat(nimi) VALUES (?);"""
ADD_PARCEL =                """INSERT INTO Paketit(koodi, asiakas_id) VALUES (?,?);"""
ADD_EVENT =                 """INSERT INTO Tapahtumat(paketti_id, paikka_id, kuvaus, ajankohta)
                               VALUES (?,?,?,datetime('now', 'localtime'));"""

GET_EVENTS_FOR_PARCEL =     """SELECT T.ajankohta, L.nimi, T.kuvaus FROM Tapahtumat T
                               LEFT JOIN Paketit as P ON P.id = T.paketti_id
                               LEFT JOIN Paikat as L ON T.paikka_id = L.id
                               WHERE P.koodi = ?;"""

GET_PARCELS_FOR_CUSTOMER =  """SELECT P.koodi, count(T.paketti_id) FROM Paketit P
                               LEFT JOIN Asiakkaat A ON P.asiakas_id = A.id
                               LEFT JOIN Tapahtumat T ON P.id = T.paketti_id
                               WHERE A.nimi = ?
                               GROUP BY P.koodi;"""

GET_PARCEL_COUNT_FOR_CUSTOMER = """SELECT A.nimi, count(P.id) FROM Paketit as P
                               LEFT JOIN Asiakkaat as A ON P.asiakas_id = A.id
                               WHERE A.nimi = ?
                               GROUP BY P.asiakas_id;"""

GET_EVENTS_PER_DATE =       """SELECT count(T.paikka_id) FROM Tapahtumat T
                               LEFT JOIN Paikat P ON T.paikka_id = P.id
                               WHERE P.nimi = ?
                               AND date(?) = date(ajankohta);"""
