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