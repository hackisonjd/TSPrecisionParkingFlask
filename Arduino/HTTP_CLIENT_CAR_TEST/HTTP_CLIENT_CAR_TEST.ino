#include <WiFi.h>
#include <WiFiClient.h>
#include <WebServer.h>
#include <ESPmDNS.h>
#include <HTTPClient.h>

//Setup ultrasonic
const int trigPin = 14;
const int echoPin = 12;
long duration = 0;
int distance = 0;
const int park_thresh = 15;
String dist;
bool occupied = false;
bool prev_occupied = false;
bool stat_change = false;
String msg = "false";
int car = 0;
String json;

//Setup Network
const char* ssid = "xlab";
const char* password = "xlabxlab";
const char* serverName = "http://10.0.0.7:8000";

WebServer server(80);

const int led = 13;

void handleRoot() {
  digitalWrite(led, 1);
  json = "{\'status\':'";
  json += msg;
  json += "\'}";
  server.send(200, "text/json", json);
  digitalWrite(led, 0);
}

void handleNotFound() {
  digitalWrite(led, 1);
  String message = "File Not Found\n\n";
  message += "URI: ";
  message += server.uri();
  message += "\nMethod: ";
  message += (server.method() == HTTP_GET) ? "GET" : "POST";
  message += "\nArguments: ";
  message += server.args();
  message += "\n";
  for (uint8_t i = 0; i < server.args(); i++) {
    message += " " + server.argName(i) + ": " + server.arg(i) + "\n";
  }
  server.send(404, "text/plain", message);
  digitalWrite(led, 0);
}

void setup(void) {
  pinMode(trigPin, OUTPUT); // Sets the trigPin as an Output
  pinMode(echoPin, INPUT); // Sets the echoPin as an Input
  pinMode(led, OUTPUT);
  digitalWrite(led, 0);
  Serial.begin(115200);
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);
  Serial.println("");

  // Wait for connection
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.print("Connected to ");
  Serial.println(ssid);
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());

  if (WiFi.status() == WL_CONNECTED) {

    if (MDNS.begin("esp32")) {
      Serial.println("MDNS responder started");
    }

    server.on("/", handleRoot);

    server.on("/inline", []() {
      server.send(200, "text/plain", "this works as well");
    });

    server.onNotFound(handleNotFound);

    server.begin();
    Serial.println("HTTP server started");
  }
}

void loop(void) {

  prev_occupied = occupied;
  // The sensor is triggered by a HIGH pulse of 10 or more microseconds.
  // Give a short LOW pulse beforehand to ensure a clean HIGH pulse:
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  // Sets the trigPin on HIGH state for 10 micro seconds
  digitalWrite(trigPin, HIGH);
  delayMicroseconds(10);
  digitalWrite(trigPin, LOW);
  // Reads the echoPin, returns the sound wave travel time in microseconds
  duration = pulseIn(echoPin, HIGH);
  // Calculating the distance
  distance = duration * 0.034 / 2;


  if (distance < park_thresh) {
    occupied = true;
  } else {
    occupied = false;
  }
  if (occupied < 2000 && prev_occupied < 2000) {
    if (occupied != prev_occupied) {
      stat_change = true;
      Serial.println("Status change");
      if (occupied) {
        msg = "true";
      } else {
        msg = "false";
      }
      WiFiClient client;
      HTTPClient http;
      int httpResponseCode;
      http.begin(client, serverName);
      http.addHeader("Content-Type", "text/plain");
      json = "{\'status\':'";
      json += msg;
      json += "\'}";
      httpResponseCode = http.POST(json);
      Serial.print(msg);
      Serial.print(", ");
      Serial.println(httpResponseCode);
      http.end();
      delay(100);
    } else {
      stat_change = false;
    }
  }
  server.handleClient();
  delay(200);//allow the cpu to switch to other tasks
}
