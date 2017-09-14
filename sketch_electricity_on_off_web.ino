#include <ESP8266WiFi.h>

IPAddress ip(XXX, XXX, X, XXX);
IPAddress gateway(XXX, XXX, X, X);
IPAddress subnet(255, 255, 255, 0);

const char* ssid = "<your ssid>";
const char* password = "<your password>";
 
int ledPin = 12; // GPIO13, D6
WiFiServer server(80);
 
void setup() {
  Serial.begin(115200);
  delay(10);
 
  pinMode(ledPin, OUTPUT);
  //digitalWrite(ledPin, LOW);
  digitalWrite(ledPin, HIGH);
 
  // Connect to WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
 
  WiFi.begin(ssid, password);
 
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected");

  // Config static ip
  WiFi.config(ip, gateway, subnet);
  
  // Start the server
  server.begin();
  Serial.println("Server started");
 
  // Print the IP address
  Serial.print("Use this URL to connect: ");
  Serial.print("http://");
  Serial.print(WiFi.localIP());
  Serial.println("/");
 
}
 
void loop() {
  // Check if a client has connected
  WiFiClient client = server.available();
  if (!client) {
    return;
  }
 
  // Wait until the client sends some data
  Serial.println("new client");
  while(!client.available()){
    delay(1);
  }
 
  // Read the first line of the request
  String request = client.readStringUntil('\r');
  Serial.println(request);
  client.flush();
 
  // Match the request
 
  if (request.indexOf("/LED=ON") > 0)  {
    digitalWrite(ledPin, LOW);
  }

  if (request.indexOf("/LED=OFF") > 0)  {
    digitalWrite(ledPin, HIGH);
  }
  
  // Return the response
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println(""); //  do not forget this one
  client.println("<!DOCTYPE HTML>");
  client.println("<html>");
  client.println("<center>");
  client.print("Electricity is now: ");
 
  if(digitalRead(ledPin)) {
    client.print("Off");
  } else {
    client.print("On");
  }
  client.println("</center>");
  client.println("<br>");
  client.println("<center>");
  client.println("<a href=\"/LED=ON\"\"><button>Turn On </button></a>");
  client.println("<a href=\"/LED=OFF\"\"><button>Turn Off </button></a><br />");  
  client.println("</html>");
  client.println("</center>");
  delay(1);
  Serial.println("Client disonnected");
  Serial.println("");
 
}
