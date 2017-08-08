#include <PubSubClient.h>
#include <DHT.h>
#include <ESP8266WiFi.h>
#include <OneWire.h>
#include <WiFiClient.h>
#include <DallasTemperature.h>
#include <Streaming.h>

// DHT Sensor connected to digital pin 5
#define DHTPIN D5
// Type of DHT sensor
#define DHTTYPE DHT22 
// Deep sleep delay
#define SLEEP_DELAY_IN_SECONDS  900 // Delay 15 minutes
// Waterproof temperature sensor
#define ONE_WIRE_BUS            D4      // DS18B20 pin

// Initialize DHT sensor
DHT dht(DHTPIN, DHTTYPE);
// network SSID (name)
char ssid[] = "<network ssid>"; 
// network password
char pass[] = "<password>"; 

// Initialize the Wifi client library
WiFiClient client;
// Initialize the PuBSubClient library
PubSubClient mqttClient(client);
// Define the MQTT broker
const char* server = "<server ip>";
const char* mqtt_username = "<mqtt username>";
const char* mqtt_password = "<mqtt password>";
const char* mqtt_topic = "<topic>";

OneWire oneWire(ONE_WIRE_BUS);
DallasTemperature DS18B20(&oneWire);

void setup() {
  // Begin serial transfer
  Serial.begin(115200);  
  dht.begin();  
  delay(10);  
  // Connect to WiFi network  
  Serial.println();  
  Serial.println();  
  Serial.print("Connecting to ");  
  Serial.println(ssid);  
  WiFi.begin(ssid, pass);  
  while (WiFi.status() != WL_CONNECTED)  
  {  
   delay(500);  
   Serial.print(".");  
  }  
  Serial.println("");  
  Serial.println("WiFi connected");  
  // Print the IP address  
  Serial.println(WiFi.localIP());  
  // Set the MQTT broker details
  mqttClient.setServer(server, 1883);
}

// Read temperature 0.2 m above ground
float getTemperature() {
  Serial << "Requesting DS18B20 temperature..." << endl;
  float temp;
  do {
    DS18B20.requestTemperatures(); 
    temp = DS18B20.getTempCByIndex(0);
    delay(100);
  } while (temp == 85.0 || temp == (-127.0));
  return temp;
}

// Read soil temperature
float getTemperature2() {
  Serial << "Requesting DS18B20 temperature..." << endl;
  float temp;
  do {
    DS18B20.requestTemperatures(); 
    temp = DS18B20.getTempCByIndex(1);
    delay(100);
  } while (temp == 85.0 || temp == (-127.0));
  return temp;
}

void loop() {
 // Check if MQTT client has connected else reconnect
  if (!mqttClient.connected()) 
  {
    reconnect();
  }
  // Call the loop continuously to establish connection to the server
  mqttClient.loop();
  
  mqttpublish();

  delay(100);  
  
  Serial << "Closing MQTT connection..." << endl;
  mqttClient.disconnect();

  Serial << "Closing WiFi connection..." << endl;
  WiFi.disconnect();

  delay(100);
  
  Serial << "Entering deep sleep mode for " << SLEEP_DELAY_IN_SECONDS << " seconds..." << endl;
  ESP.deepSleep(SLEEP_DELAY_IN_SECONDS * 1000000, WAKE_RF_DEFAULT);

  delay(500);   // wait for deep sleep to happen
}

void reconnect() 
{
  // Loop until we're reconnected
  while (!mqttClient.connected()) 
  {
    Serial.print("Attempting MQTT connection...");
    // Connect to the MQTT broker
    if (mqttClient.connect("ESP8266Client",mqtt_username, mqtt_password)) 
    {
      Serial.println("connected");
    } else 
    {
      Serial.print("failed, rc=");
      // Print to know why the connection failed
      // See http://pubsubclient.knolleary.net/api.html#state for the failure code and its reason
      Serial.print(mqttClient.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying to connect again
      delay(5000);
    }
  }
}

void mqttpublish() {
  // Read temperature from DHT sensor, Fahrenheit if dht.readTemperature(true)
  float t = dht.readTemperature();
  // Cut data length of all values. Last values in string are not othervise accepted.  
  String t_s = String(t, DEC);
  t_s = t_s.substring(0,7);

  // Read humidity from DHT sensor
  float h = dht.readHumidity();
  String h_s = String(h, DEC);
  h_s = h_s.substring(0,7);

  // Read from waterproof one wire temperature sensors
  // Read temperature 0.2 m above ground
  float t2 = getTemperature();
  String t2_s = String(t2, DEC);
  t2_s = t2_s.substring(0,7);
  // Read soil temperature
  float t3 = getTemperature2();
  String t3_s = String(t3, DEC);
  t3_s = t3_s.substring(0,7);
  
  // Create data string to send to ThingSpeak
  String data = String("field1=" + t_s + "&field2=" + h_s + "&field3=" + t2_s + "&field4=" + t3_s);
  // Get the data string length
  int length = data.length();
  char msgBuffer[length];
  // Convert data string to character buffer
  data.toCharArray(msgBuffer,length+1);
  Serial.println(msgBuffer);

  // Publish data to local broker.
  mqttClient.publish(mqtt_topic,msgBuffer);
  delay(500);
}
