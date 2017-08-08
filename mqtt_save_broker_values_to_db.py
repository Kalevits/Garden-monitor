#!/usr/bin/python3

import paho.mqtt.client as mqtt #import the client1
import time
import mysql.connector
import mqtt_send_garden_data

def save_to_db(msg):
    conn = mysql.connector.connect(user='<username>', password='<password>', database='<databasename>')
    cursor = conn.cursor()
    new_conditions = ('INSERT INTO olosuhteet '
        '(temperature, humidity, temp_20cm, soil_temperature, soil_humidity, gh_temperature,'
        'gh_soil_humidity, water_level) '
        'VALUES (%s, %s, %s, %s, %s, %s, %s, %s)')
    # Set default values
    mystring1 = None
    mystring2 = None
    mystring3 = None
    mystring4 = None
    mystring5 = None
    mystring6 = None
    mystring7 = None
    mystring8 = None

    # Add values to value list. Split by &
    list1 = msg.split('&')
    ####
    for ind in range(len(list1)):
        # Split field and value. Split by =  
        list2 = list1[ind].split('=')
        fieldstring = list2[0]
        valuestring = list2[1]
        if (fieldstring == 'field1'):
            mystring1 = valuestring
        elif (fieldstring == 'field2'):
            mystring2 = valuestring
        elif (fieldstring == 'field3'):
            mystring3 = valuestring
        elif (fieldstring == 'field4'):
            mystring4 = valuestring
        elif (fieldstring == 'field5'):
            mystring5 = valuestring
        elif (fieldstring == 'field6'):
            mystring6 = valuestring
        elif (fieldstring == 'field7'):
            mystring7 = valuestring
        elif (fieldstring == 'field8'):
            mystring8 = valuestring
        else:
            print('Halavatun virhe')

    ####
    # Add values to execute
    condition = (mystring1, mystring2, mystring3, mystring4, mystring5, mystring6, mystring7, mystring8)
    #print(condition)
    
    try:
        cursor.execute(new_conditions, condition)
        conn.commit()
    except Exception as open_error:
        error_file = open('/home/pi/py3production/error/errors.txt', 'a')
        error_file.write(open_error)
        error_file.close()
        return('Sorry, there was a problem adding the data')
    else:
        return('Data values added!')
    cursor.close()
    conn.close()

############
def on_message(client, userdata, message):
    print("message received " ,str(message.payload.decode("utf-8")))
    print("message topic=",message.topic)
    print("message qos=",message.qos)
    print("message retain flag=",message.retain)
    msg = str(message.payload.decode("utf-8"))
    # Save data to mysql database
    save_result = save_to_db(msg)
    print(save_result)
    # Send data to thingspeak
    send_result = mqtt_send_garden_data.send_to_thingspeak(msg)
    print(send_result)
    
############
broker_address="localhost"

print("creating new instance")
client = mqtt.Client("P1") #create new instance
client.on_message=on_message #attach function to callback
print("connecting to broker")
client.connect(broker_address) #connect to broker
#client.loop_start() #start the loop
print("Subscribing to topic","sensors/test/temperature")
client.subscribe("sensors/test/temperature")
time.sleep(10) # wait
client.loop_forever() #start the loop
