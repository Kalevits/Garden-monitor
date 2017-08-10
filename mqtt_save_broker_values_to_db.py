#!/usr/bin/python3

import mysql.connector

def save_to_db(msg):
    conn = mysql.connector.connect(user='<user>', password='<password>', database='<database name>')
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
