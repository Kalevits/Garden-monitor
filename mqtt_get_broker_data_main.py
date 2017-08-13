#!/usr/bin/python3

import paho.mqtt.client as mqtt #import the client1
import time
import mqtt_save_broker_values_to_db
import mqtt_send_garden_data

############
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    msg = str(message.payload.decode("utf-8"))
    # Save data to mysql database
    save_result = mqtt_save_broker_values_to_db.save_to_db(msg)
    print(save_result)
    # Send data to thingspeak
    send_result = mqtt_send_garden_data.send_to_thingspeak(msg)
    print(send_result)
    
############
def main():
    broker_address="localhost"

    print("creating new instance")
    client = mqtt.Client() #create new instance
    client.on_message=on_message #attach function to callback
    print("connecting to broker")
    client.connect(broker_address) #connect to broker
    #client.loop_start() #start the loop
    print("Subscribing to topic","sensors/test/temperature")
    client.subscribe("sensors/test/temperature")
    time.sleep(10) # wait
    client.loop_forever() #start the loop

main()
