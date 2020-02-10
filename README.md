# Tikape harjoitustyö 2020

Juhani Riisiö, `opnro`, `tunnus`

## Toiminnot

- [1] Luo sovelluksen tarvitsemat taulut tyhjään tietokantaan.
- [2] Lisää uusi paikka tietokantaan, kun annetaan paikan nimi.
- [3] Lisää uusi asiakas tietokantaan, kun annetaan asiakkaan nimi.
- [4] Lisää uusi paketti tietokantaan, kun annetaan paketin seurantakoodi ja asiakkaan nimi. Asiakkaan tulee olla valmiiksi tietokannassa.
- [5] Lisää uusi tapahtuma tietokantaan, kun annetaan paketin seurantakoodi, tapahtuman paikka sekä kuvaus. Paketin ja paikan tulee olla valmiiksi tietokannassa.
- [6] Hae kaikki paketin tapahtumat seurantakoodin perusteella.
- [7] Hae kaikki asiakkaan paketit ja niihin liittyvien tapahtumien määrä.
- [8] Hae annetusta paikasta tapahtumien määrä tiettynä päivänä.
- [9] Suorita tietokannan tehokkuustesti (tästä lisää alempana).

## Tehokkuustesti

lorem ipsum

## Rajoitteet

Asiakkaiden ja paikkojen nimillä sekä pakettien koodeilla on tietokantatasolla rajoite UNIQUE, jolloin samannimiset lisäykset aiheuttavat poikkeuksen. Useiden samanaikaisten käyttäjien tapauksessa ei tulisi olla ongelmaa sillä kirjoituskomennot ovat yksittäisiä käskyjä, jolloin ne muodostavat itsessään transaktion. SQLiten oletustransaktiotaso on 4, eli ainoastaan yksi säie voi lukea tai kirjoittaa tietokantaan yhdellä hetkellä. Täsmälleen samanaikaiset kirjoituskäskyt suoritetaan joka tapauksessa jossain peräkkäisessä järjestyksessä, jolloin esim. samaa paikannimeä kirjoittavista käskyistä jälkimmäinen saa `unique constraint violation` poikkeuksen.
