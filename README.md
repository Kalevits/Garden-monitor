# Garden-monitor

This is still under construction and that's why this is updated all the time.

This system reads garden temperature and moisture contents and saves data to MySQL-database and sends information to ThingSpeak. This also allows to controll different functions like irrigation.

File explanations:
- Puutarhan seurantajärjestelmä.pdf: General description
- mqtt_get_broker_data_main.py: Python program, that reads the data that NodeMCU-units have sent to Mosquitto-broker.
- mqtt_save_broker_values_to_db.py: Python module, which saves values to MySQL-database. mqtt_get_broker_data_main.py uses this.
- mqtt_send_garden_data.py: Python module, which sends values to ThingSpeak. mqtt_get_broker_data_main.py uses this.
- sketch_may23a_mqtt_deep_sleep_omaserveri.ino: NodeMCU-Arduino -program, which reads data from sensors and sends them to broker.
- puutarhagraafit.cgi: Python-program, that shows results as CanvasJS-graphs. Timespan of selection can be 1-16 weeks.
- garden_server.html: Html-page to show controls collection and sea level forecast.
