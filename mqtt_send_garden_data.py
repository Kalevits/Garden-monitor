#!/usr/bin/python3

from __future__ import print_function
import paho.mqtt.publish as publish
#import psutil

def send_to_thingspeak(message):
    # The ThingSpeak Channel ID
    # Garden monitor
    channelID = "<channelid>"
    
    # The Write API Key for the channel
    # Garden monitor
    apiKey = "<apikey>"

    # The Hostname of the ThinSpeak MQTT broker
    mqttHost = "mqtt.thingspeak.com"

    tTransport = "websockets"
    tPort = 80

    # Create the topic string
    topic = "channels/" + channelID + "/publish/" + apiKey

    # attempt to publish this data to the topic 
    try:
        publish.single(topic, message, hostname=mqttHost, transport=tTransport, port=tPort)
    except Exception as open_error:
        error_file = open('/home/pi/py3production/error/errors.txt', 'a')
        error_file.write(open_error)
        error_file.close()
        return("There was an error while publishing the data.")
    else:
        return("Data sent to ThingSpeak")
