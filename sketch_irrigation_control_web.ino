#include <ESP8266WiFi.h>

IPAddress ip(XXX, XXX, X, XXX);
IPAddress gateway(XXX, XXX, X, X);
IPAddress subnet(255, 255, 255, 0);


const char* ssid = "<your ssid>";
const char* password = "<your password>";
 
WiFiServer server(80);
 
void setup() {
  Serial.begin(115200);
  delay(10);
  pinMode(5, OUTPUT); // D1
  pinMode(4, OUTPUT); // D2
  pinMode(0, OUTPUT); // D3
  pinMode(13, OUTPUT); // D7

  digitalWrite(5, HIGH);
  digitalWrite(4, HIGH);
  digitalWrite(0, HIGH);
  digitalWrite(13, HIGH);
   
  // Connect to WiFi network
  Serial.println();
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);

  // Connect to network
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
  if (request.indexOf("/light1on") > 0)  {
    digitalWrite(5, LOW);
  }
  if (request.indexOf("/light1off") >0)  {
    digitalWrite(5, HIGH);
  }
   if (request.indexOf("/light2on") > 0)  {
    digitalWrite(4, LOW);
  }
  if (request.indexOf("/light2off") >0)  {
    digitalWrite(4, HIGH);
  }
    if (request.indexOf("/light3on") >0)  {
    digitalWrite(0, LOW);
  }
  if (request.indexOf("/light3off") > 0)  {
    digitalWrite(0, HIGH);
  }
   if (request.indexOf("/light4on") > 0)  {
    digitalWrite(13, LOW);
  }
  if (request.indexOf("/light4off") > 0)  {
    digitalWrite(13, HIGH);
  }

  // Return the response
  client.println("HTTP/1.1 200 OK");
  client.println("Content-Type: text/html");
  client.println(""); //  do not forget this one
  client.println("<!DOCTYPE HTML>");
  client.println("<html>");
  client.println("<hr/><hr>");
  client.println("<h4><center> Irrigation Control Center</center></h4>");
  client.println("<hr/><hr>");
  //client.println("<br><br>");
  client.println("<center>");
  client.println("Device 1");
  client.println("<a href=\"/light1on\"\"><button>Turn On </button></a>");
  client.println("<a href=\"/light1off\"\"><button>Turn Off </button></a><br />");  
  client.println("</center>");   
  //client.println("<br><br>");
   client.println("<center>");
   client.println("Device 2");
  client.println("<a href=\"/light2on\"\"><button>Turn On </button></a>");
  client.println("<a href=\"/light2off\"\"><button>Turn Off </button></a><br />");  
  client.println("</center>"); 
  //client.println("<br><br>");
  client.println("<center>");
  client.println("Device 3");
  client.println("<a href=\"/light3on\"\"><button>Turn On </button></a>");
  client.println("<a href=\"/light3off\"\"><button>Turn Off </button></a><br />");  
  client.println("</center>"); 
  //client.println("<br><br>");
  client.println("<center>");
  client.println("Device 4");
  client.println("<a href=\"/light4on\"\"><button>Turn On </button></a>");
  client.println("<a href=\"/light4off\"\"><button>Turn Off </button></a><br />");  
  client.println("</center>"); 
  //client.println("<br><br>");
  client.println("<center>");
  client.println("<table border=\"5\">");
 client.println("<tr>");
  if (digitalRead(5))
         { 
           client.print("<td>Device 1 is OFF</td>");
         }
          else
          {
            client.print("<td>Device 1 is ON</td>");
        }
        client.println("<br />");
         if (digitalRead(4))
          { 
           client.print("<td>Device 2 is OFF</td>");
         }
          else
          {
            client.print("<td>Device 2 is ON</td>");
          }
          client.println("</tr>");
          client.println("<tr>");
          if (digitalRead(0))
          { 
           client.print("<td>Device 3 is OFF</td>");
          }
          else
          {
            client.print("<td>Device 3 is ON</td>");
          }
          if (digitalRead(13))
          { 
           client.print("<td>Device 4 is OFF</td>");
          }
          else
          {
            client.print("<td>Device 4 is ON</td>");
          }
          client.println("</tr>");
          client.println("</table>");
          client.println("</center>");
  client.println("</html>"); 
  delay(1);
  Serial.println("Client disonnected");
  Serial.println("");
 
}
