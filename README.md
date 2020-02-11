# Tikape harjoitustyö 2020

Juhani Riisiö, `opnro`, `tunnus`

## Toiminnot

- [1] Luo sovelluksen tarvitsemat taulut tyhjään tietokantaan.
- [2] Lisää uusi paikka tietokantaan, kun annetaan paikan nimi.
- [3] Lisää uusi asiakas tietokantaan, kun annetaan asiakkaan nimi.
- [4] Lisää uusi paketti tietokantaan, kun annetaan paketin seurantakoodi ja asiakkaan nimi.
- [5] Lisää uusi tapahtuma tietokantaan, kun annetaan paketin seurantakoodi, tapahtuman paikka sekä kuvaus.
- [6] Hae kaikki paketin tapahtumat seurantakoodin perusteella.
- [7] Hae kaikki asiakkaan paketit ja niihin liittyvien tapahtumien määrä.
- [8] Hae annetusta paikasta tapahtumien määrä tiettynä päivänä.
- [9] Suorita tietokannan tehokkuustesti.

## Tehokkuustesti

Ilman indeksejä:
- Vaihe 1: 0.0067127799993613735 s
- Vaihe 2: 0.002624913000545348 s
- Vaihe 3: 0.005789549999462906 s
- Vaihe 4: 9.153414673000043 s
- Vaihe 5: 0.1412476109999261 s
- Vaihe 6: 135.65182855700004 s

Indeksien kanssa:
- Vaihe 1: 0.005237512000348943 s
- Vaihe 2: 0.005851029999575985 s
- Vaihe 3: 0.008006899999600137 s
- Vaihe 4: 17.88824620500054 s
- Vaihe 5: 0.10688023500006238 s
- Vaihe 6: 105.48912531600035 s

Näyttäisi siltä, että kirjoitustoiminnot 1-4 ovat indeksien kanssa hieman hitaampia, joka olisi odotetun mukaista. Vaihe 5, jossa haetaan asiakkaalle kuuluvien pakettien lukumäärää allaolevalla kyselyllä, on n. 30% nopeampi kun asiakkaan nimessä on indeksi.

```sql
SELECT A.nimi, count(P.id) FROM Paketit as P
LEFT JOIN Asiakkaat as A ON P.asiakas_id = A.id
WHERE A.nimi = ?
GROUP BY P.asiakas_id;
```

Vaihe 6 käyttää allaolevaa kyselyä ja on diabolisen hidas. Parannusta indeksin kanssa tulee n. 20%, joskin luvuissa on vaihtelua ajojen välillä. Indeksit liittyvät paketin koodiin ja paketti_id sekä paikka_id kenttiin.

```sql
SELECT T.ajankohta, L.nimi, T.kuvaus FROM Tapahtumat T
LEFT JOIN Paketit as P ON P.id = T.paketti_id
LEFT JOIN Paikat as L ON T.paikka_id = L.id
WHERE P.koodi = ?;
```

## Rajoitteet

Asiakkaiden ja paikkojen nimillä sekä pakettien koodeilla on tietokantatasolla rajoite UNIQUE, jolloin samanarvoiset lisäykset aiheuttavat poikkeuksen. Useiden samanaikaisten käyttäjien tapauksessa ei tulisi olla ongelmaa ainakaan tiedon eheyden suhteen, sillä kirjoituskomennot ovat yksittäisiä käskyjä, jolloin ne muodostavat itsessään transaktion. SQLiten oletustransaktiotaso on serialisoitu, eli ainoastaan yksi säie voi lukea tai kirjoittaa tietokantaan yhdellä hetkellä. Täsmälleen samanaikaiset kirjoituskäskyt suoritetaan joka tapauksessa jossain peräkkäisessä järjestyksessä, jolloin esim. samaa paikannimeä kirjoittavista käskyistä jälkimmäinen aiheuttaa `unique constraint violation` poikkeuksen.
