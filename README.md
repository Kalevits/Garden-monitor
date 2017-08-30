# Garden-monitor

Tämä on vielä puolivalmis ja lisää osia lisätään sitä mukaa kuin niitä saadaan valmiiksi. 

Tämä järjestelmä lukee lämpötila- ja kosteusarvoja puutarhasta ja tallentaa tiedot tietokantaan sekä lähettää tiedot ThingSpeakiin. Järjestelmällä voi myös etäohjata puutarhan toimintoja, kuten kastelua.

Tiedostojen selitys:
- Puutarhan seurantajärjestelmä.pdf: Yleinen kuvaus
- mqtt_get_broker_data_main.py: Python ohjelma, joka lukee NodeMCU-yksiköiden lähettämän datan Mosquitto-brokerilta.
- mqtt_save_broker_values_to_db.py: Python moduli, joka tallentaa arvot MySQL-kantaan. mqtt_get_broker_data_main.py käyttää tätä.
- mqtt_send_garden_data.py: Python moduli, joka lähettää arvot ThingSpeakiin. mqtt_get_broker_data_main.py käyttää tätä.
- sketch_may23a_mqtt_deep_sleep_omaserveri.ino: NodeMCU-Arduino -ohjelma, joka lukee tiedot mittausantureilta ja lähettää ne brokerille.
- puutarhagraafit.cgi: Python-moduli, joka näyttää mittaustulokset CanvasJS-kuvaajina. Kuvausväliksi voi valita 1-16 viikkoa.
