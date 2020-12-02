# tsoha-blog

Harjoitustyöni on blogialusta muutamalla toiminnallisuudella:

Blogissa on mahdollisuus tehdä kolmenlaisia postauksia: lyhyt yhden kuvan pikapostaus (löytyy etusivulta), perinteinen pidempi blogipostaus kommentointialueella joka ladotaan kuvista ja tekstistä halutussa järjestyksessä, sekä lyhyt postaus joka näkyy vain kirjautuneille käyttäjille joilla on adminin hyväksyntä (tarkoituksena luoda ympäristö sisällölle, jota ei haluta kaikkien saataville).

Käyttäjiä on neljässä kategoriassa:
1. Käyttäjä, joka ei ole kirjautunut voi
  * nähdä etusivun ja pidemmät blogipostaukset
  * lähettää yksityisen viestin adminille
2. Käyttäjä, joka on kirjautunut voi lisäksi
  * kommentoida jokaista näkemäänsä postausta
  * vaihtaa tilinsä käyttäjänimen tai salasanan oman tilin hallintasivulta
  * poistaa tilinsä järjestelmästä
3. Käyttäjä, joka on kirjautunut ja on ylläpidon hyväksymä voi lisäksi
  * nähdä kolmannen sisältöalueen, jossa etusivun kaltainen sisällönjakelu
  * luoda uutta sisältöä niiden tekoon soveltuvilla sivuilla
4. Admin voi lisäksi
  * poistaa postauksia
  * poistaa kommentteja (admin ei pysty kommentoimaan postauksia)
  * hallinnoida käyttäjien tietoja heidän omilta sivuiltaan
  * vaihtaa käyttäjän käyttäjäryhmän tai poistaa käyttäjä järjestelmästä
  * lukea ylläpidolle tulleita viestejä
  * poistaa em. viestejä
  
  
  ----------


Sovellusta voi testata osoitteessa https://pure-shelf-99302.herokuapp.com/


Näkymät ja toiminnot sovelluksen käyttäjäryhmiin saa seuraavilla testikäyttäjätunnuksilla:
* admin g6LEWTkMpnL7hP
* perus 624v9sGWG84sjg
* luoja p4srDNiimn46J3


 -----------
 
 
 Sovellus on toteutettu yksinkertaistaen Pythonilla: Flask-kirjasto jakelee Jinjalla koottuja html-pohjia joihin haetaan blogin sisältö PostgreSQL-tietokannasta. Ulkoasu on käytännössä kokonaan Bootstrapin varassa, custom.css-tiedostossa on pari overridea jotta sivut näyttäisivät hieman persoonallisemmilta ja rauhallisilta. Sovellus on pilkottu seuraavanlaisesti osiin: app.py on sovelluksen pää, routes.py hoitaa get- ja post-pyynnöt ja hakee sisältöä muista moduuleista; viestit messages-moduulista, kommentit comments-moduulista jne.. HTML-tiedostot kasataan seuraavasti: layout.html on jokaisen sivun pohjana, siihen ladotaan /templates/partials-kansiosta aina navbar.html sekä login.html mikäli käyttäjä ei ole kirjautunut sisään sekä itse sivusto jota käyttäjä hakee selaimellaan. 
 
Sovelluksen saa käyttöön itselleen kopioimalla repositorion, asentamalla riippuvuudet ja määrittelemällä .env-tiedostoon tietokannan osoite sekä salainen avain jotka sovellus hakee käynnistyessään. Kun sovellus otetaan ensimmäistä kertaa käyttöön, tietokannasta ei löydy admin-käyttäjää. Admin-käyttäjä luodaan järjestelmään blogin rekisteröidy-sivulla ja ajetaan tietokannassa komento "UPDATE users SET user_group = 'admin' WHERE username = '(käyttäjänimi)';. Kun ensimmäinen admin on luotu, voi tällä tilillä muuttaa muiden käyttäjien käyttäjäryhmiä.
