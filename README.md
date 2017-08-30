# Garden-monitor

Tämä on vielä puolivalmis ja lisää osia lisätään sitä mukaa kuin niitä saadaan valmiiksi. 

Tämä järjestelmä lukee lämpötila- ja kosteusarvoja puutarhasta ja tallentaa tiedot tietokantaan sekä lähettää tiedot ThingSpeakiin. Järjestelmällä voi myös etäohjata puutarhan toimintoja, kuten kastelua.

Tiedostojen selitys:
- Puutarhan seurantajärjestelmä.pdf: Yleinen kuvaus
- mqtt_get_broker_data_main.py: Lukee NodeMCU-yksiköiden lähettämän datan Mosquitto-brokerilta.
- mqtt_save_broker_values_to_db.py: Tallentaa arvot MySQL-kantaan. mqtt_get_broker_data_main.py käyttää tätä.
- mqtt_send_garden_data.py: Lähettää arvot ThingSpeakiin. mqtt_get_broker_data_main.py käyttää tätä.
- sketch_may23a_mqtt_deep_sleep_omaserveri.ino: NodeMCU-ohjelma, joka lukee tiedot ja lähettää ne brokerille.
