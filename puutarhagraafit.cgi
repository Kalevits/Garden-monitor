#!/usr/bin/python3

import mysql.connector
import json
import collections
import datetime
import os
import cgi
import cgitb

# Print http page headers
def printHTTPheader():
    print('''Content-Type: text/html

    <!DOCTYPE html>
    <html>
    <head>

    <title>Garden results</title>

    </head>
    <h2>Garden data</h2>
    <body>

    ''')

# Format data for JSON readable format    
def datetime_handler(x):
    if isinstance(x, datetime.datetime):
        return x.isoformat()
    raise TypeError("Unknown type")

# Get data from database
def fetch_data(interval):
    
    conn = mysql.connector.connect(user='<user>', password='<user password>', database='<database name>')
    cursor = conn.cursor()

    query = ('SELECT date, temperature, humidity, temp_20cm, soil_temperature, soil_humidity, gh_temperature, gh_soil_humidity ')
    query = query + ('FROM olosuhteet WHERE date>NOW() - INTERVAL %s WEEK AND date<=NOW() ORDER BY date DESC' % interval) 
    cursor.execute(query)

    data = cursor.fetchall()

    cursor.close()
    conn.close()

    #Converting data into json
    temperature_list = []
    for row in data :
        d = collections.OrderedDict()
        d['date']  = row[0] #date
        d['temperature']   = row[1] #temperature
        d['humidity']   = row[2] #humidity
        d['temp_20cm']   = row[3] #temperature above ground
        d['soil_temperature']   = row[4] #soil temperature
        d['soil_humidity']   = row[5] #soil humidity
        d['gh_temperature']   = row[6] #greenhouse temperature
        d['gh_soil_humidity']   = row[7] #greenhouse soil humidity
        temperature_list.append(d)

    #return json.dumps(temperature_list). Contains all necessary data
    j = json.dumps(temperature_list, default=datetime_handler)
    json_data = open('/var/www/html/json_list.json','w')
    json_data.write(j)
    json_data.close()

# Print CanvasJS graphs
def print_graphs():
    
    print('''
    <script src="http://localhost/jquery-3.2.1.min.js"></script>
    <script type="text/javascript" src="http://localhost/canvasjs.min.js"></script>
    <script type="text/javascript">
    window.onload = function () {
    var dataPoints1 = [];
    $.getJSON("http://localhost/json_list.json", function(data) {  
            $.each(data, function(key, value){
                if(value.temperature != null)
                {
                    dataPoints1.push({x: new Date(value.date), y: Number(value.temperature)});
                    }
            });
            var chart1 = new CanvasJS.Chart("chartContainer1",{
                    title:{
                            text:"Air temperature"
                    },
                    data: [{
                            type: "line",
                            dataPoints : dataPoints1,
                    }]
            });
            chart1.render();
       });

    var dataPoints2 = [];
    $.getJSON("http://localhost/json_list.json", function(data) {  
            $.each(data, function(key, value){
                if(value.humidity != null)
                {
                    dataPoints2.push({x: new Date(value.date), y: Number(value.humidity)});
                    }
            });
            var chart2 = new CanvasJS.Chart("chartContainer2",{
                    title:{
                            text:"Air humidity"
                    },
                    data: [{
                            type: "line",
                            dataPoints : dataPoints2,
                    }]
            });
            chart2.render();
       });

    var dataPoints3 = [];
    $.getJSON("http://localhost/json_list.json", function(data) {  
            $.each(data, function(key, value){
                if(value.temp_20cm != null)
                {
                    dataPoints3.push({x: new Date(value.date), y: Number(value.temp_20cm)});
                    }
            });
            var chart3 = new CanvasJS.Chart("chartContainer3",{
                    title:{
                            text:"Temperature 20 cm above ground"
                    },
                    data: [{
                            type: "line",
                            dataPoints : dataPoints3,
                    }]
            });
            chart3.render();
       });

    var dataPoints4 = [];
    $.getJSON("http://localhost/json_list.json", function(data) {  
            $.each(data, function(key, value){
                if(value.soil_temperature != null)
                {
                    dataPoints4.push({x: new Date(value.date), y: Number(value.soil_temperature)});
                    }
            });
            var chart4 = new CanvasJS.Chart("chartContainer4",{
                    title:{
                            text:"Soil temperature"
                    },
                    data: [{
                            type: "line",
                            dataPoints : dataPoints4,
                    }]
            });
            chart4.render();
       });

    var dataPoints5 = [];
    $.getJSON("http://localhost/json_list.json", function(data) {  
            $.each(data, function(key, value){
                if(value.soil_humidity != null)
                {
                    dataPoints5.push({x: new Date(value.date), y: Number(value.soil_humidity)});
                    }
            });
            var chart5 = new CanvasJS.Chart("chartContainer5",{
                    title:{
                            text:"Soil humidity"
                    },
                    data: [{
                            type: "line",
                            dataPoints : dataPoints5,
                    }]
            });
            chart5.render();
       });
       
    var dataPoints6 = [];
    $.getJSON("http://localhost/json_list.json", function(data) {  
            $.each(data, function(key, value){
                if(value.gh_temperature != null)
                {
                    dataPoints6.push({x: new Date(value.date), y: Number(value.gh_temperature)});
                    }
            });
            var chart6 = new CanvasJS.Chart("chartContainer6",{
                    title:{
                            text:"Greenhouse temperature"
                    },
                    data: [{
                            type: "line",
                            dataPoints : dataPoints6,
                    }]
            });
            chart6.render();
       });
       
    var dataPoints7 = [];
    $.getJSON("http://localhost/json_list.json", function(data) {  
            $.each(data, function(key, value){
                if(value.gh_soil_humidity != null)
                {
                    dataPoints7.push({x: new Date(value.date), y: Number(value.gh_soil_humidity)});
                    }
            });
            var chart7 = new CanvasJS.Chart("chartContainer7",{
                    title:{
                            text:"Greenhouse soil humidity"
                    },
                    data: [{
                            type: "line",
                            dataPoints : dataPoints7,
                    }]
            });
            chart7.render();
       });
      }
           
    </script>

    <div id="chartContainer1" style="width: 45%; height: 300px;display: inline-block;"></div> 
    <div id="chartContainer2" style="width: 45%; height: 300px;display: inline-block;"></div><br/>
    <div id="chartContainer3" style="width: 45%; height: 300px;display: inline-block;"></div>
    <div id="chartContainer4" style="width: 45%; height: 300px;display: inline-block;"></div><br/>
    <div id="chartContainer5" style="width: 45%; height: 300px;display: inline-block;"></div>
    <div id="chartContainer6" style="width: 45%; height: 300px;display: inline-block;"></div><br/>
    <div id="chartContainer7" style="width: 45%; height: 300px;display: inline-block;"></div>

    ''')

# Print graph time selection buttons
def print_time_selector(option):

    print ('''<form action="/cgi-bin/puutarhagraafit.cgi" method="POST">
        Show the environmental information logs for  
        <select name="timeinterval">''')

    if option is not None:

        if option == "1":
            print ("<option value=\"1\" selected=\"selected\">the last 1 weeks</option>")
        else:
            print ("<option value=\"1\">the last 1 weeks</option>")

        if option == "2":
            print ("<option value=\"2\" selected=\"selected\">the last 2 weeks</option>")
        else:
            print ("<option value=\"2\">the last 2 weeks</option>")

        if option == "3":
            print ("<option value=\"3\" selected=\"selected\">the last 3 weeks</option>")
        else:
            print ("<option value=\"3\">the last 3 weeks</option>")
        if option == "4":
            print ("<option value=\"4\" selected=\"selected\">the last 4 weeks</option>")
        else:
            print ("<option value=\"4\">the last 4 weeks</option>")
        if option == "8":
            print ("<option value=\"8\" selected=\"selected\">the last 8 weeks</option>")
        else:
            print ("<option value=\"8\">the last 8 weeks</option>")
        if option == "12":
            print ("<option value=\"12\" selected=\"selected\">the last 12 weeks</option>")
        else:
            print ("<option value=\"12\">the last 12 weeks</option>")
        if option == "16":
            print ("<option value=\"16\" selected=\"selected\">the last 16 weeks</option>")
        else:
            print ("<option value=\"16\">the last 16 weeks</option>")

    else:
        print ('''<option value="1">the last 1 weeks</option>
            <option value="2">the last 2 weeks</option>
            <option value="3">the last 3 weeks</option>
            <option value="4" selected="selected">the last 4 weeks</option>
            <option value="8">the last 8 weeks</option>
            <option value="12">the last 12 weeks</option>
            <option value="16">the last 16 weeks</option>''')

    print ('''</select>
        <input type="submit" value="Display"><br><br><hr>
        </form>''')

# return the option passed to the script
def get_option():
    form=cgi.FieldStorage()
    if "timeinterval" in form:
        option = form["timeinterval"].value
        return option
    else:
        return None

# Page printing     
def main():

    cgitb.enable()
    
    # Print header section
    printHTTPheader()

    # get options that may have been passed to this script
    option=get_option()

    if option is None:
        option = str(4)
        
    print_time_selector(option)
        
    # Read data from database
    fetch_data(option)

    # Print graphs
    print_graphs()

    print('</body>')
    print('</html>')

main()
