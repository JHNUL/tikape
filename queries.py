INIT_DB = """ DROP TABLE IF EXISTS Asiakas;
              DROP TABLE IF EXISTS Paikka;
              DROP TABLE IF EXISTS Paketti;
              DROP TABLE IF EXISTS Tapahtuma;
              CREATE TABLE Asiakas (
                id INTEGER PRIMARY KEY,
                nimi TEXT NOT NULL UNIQUE
              );
              CREATE TABLE Paikka (
                id INTEGER PRIMARY KEY,
                nimi TEXT NOT NULL UNIQUE
              );
              CREATE TABLE Paketti (
                koodi VARCHAR(200) PRIMARY KEY,
                asiakas_id INTEGER,
                FOREIGN KEY(asiakas_id) REFERENCES Asiakas(id)
              );
              CREATE TABLE Tapahtuma (
                id INTEGER PRIMARY KEY,
                kuvaus TEXT,
                ajankohta TEXT NOT NULL,
                paketti_koodi VARCHAR(200),
                paikka_id INTEGER,
                FOREIGN KEY(paketti_koodi) REFERENCES Paketti(id),
                FOREIGN KEY(paikka_id) REFERENCES Paikka(id)
              ); """

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