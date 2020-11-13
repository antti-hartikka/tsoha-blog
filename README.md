# tsoha-blog

Harjoitustyöni tulee olemaan blogialusta muutamalla toiminnallisuudella:

Blogissa on mahdollisuus tehdä kolmenlaisia postauksia: lyhyt yhden kuvan/videon pikapostaus kuvatekstillä (löytyy etusivulta), perinteinen pidempi blogipostaus joka ladotaan kuvista, videoista ja tekstistä halutussa järjestyksessä, sekä lyhyt postaus joka näkyy vain kirjautuneille käyttäjille joilla on adminin hyväksyntä (tarkoituksena luoda ympäristö sisällölle, jota ei haluta kaikkien saataville).

Käyttäjiä on neljässä kategoriassa:
1. Käyttäjä, joka ei ole kirjautunut.
  * Näkee etusivun ja pidemmät blogipostaukset.
  * Voi lähettää yksityisen viestin adminille.
2. Käyttäjä, joka on kirjautunut.
  * Voi lisäksi kommentoida jokaista näkemäänsä postausta.
  * Vaihtaa tilinsä käyttäjänimen tai salasanan.
3. Käyttäjä, joka on kirjautunut ja on ylläpidon hyväksymä.
  * Edellisten lisäksi näkee kolmannen sisältöalueen.
  * Voi luoda uutta sisältöä.
  * Voi muokata tai poistaa tekemäänsä sisältöä.
4. Admin.
  * Edellisten lisäksi voi muokata tai poistaa muiden tekemää sisältöä.
  * Muokata käyttäjien tietoja tai poistaa käyttäjän.
  * Voi poistaa kommentteja
  
  
  ----------


Sovellusta voi testata osoitteessa https://pure-shelf-99302.herokuapp.com/.
Sovelluksen sivut ovat "hieman" vaiheessa, sovellukseen pystyy kuitenkin mm. kirjautumaan sisään ja tarkastelemaan erilaisia näkymiä eri käyttäjäryhmien näkökulmasta.

Näkymät sovelluksen käyttäjäryhmiin saa seuraavilla testikäyttäjätunnuksilla:
* admin g6LEWTkMpnL7hP
* perus 624v9sGWG84sjg
* luoja p4srDNiimn46J3

Koodi on tällä hetkellä jäsennelty huonosti ja tavoitteena onkin refaktorointi ensi viikolla.