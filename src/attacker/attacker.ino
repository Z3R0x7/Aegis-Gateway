/**
 * AEGIS GATEWAY - Physical Layer Simulator (Charger Side)
 * Track B: Secure Plug & Charge Protocol
 * * Hardware: Arduino Uno R3, SSD1306 OLED, IRF520 MOSFET
 */

#include <Wire.h>
#include <Adafruit_GFX.h>
#include <Adafruit_SSD1306.h>

#define SCREEN_WIDTH 128
#define SCREEN_HEIGHT 64
Adafruit_SSD1306 display(SCREEN_WIDTH, SCREEN_HEIGHT, &Wire, -1);

// Pin Configuration
const int potPin = A0;      // Simulation Toggle (Safe vs Attack)
const int signalOut = 9;   // Control Pilot (CP) Line to Pico
const int picoIn = 2;      // Security Decision from Pico
const int mosfetPin = 10;  // High-Voltage Power Gate

void setup() {
  Serial.begin(9600);
  pinMode(signalOut, OUTPUT);
  pinMode(picoIn, INPUT);
  pinMode(mosfetPin, OUTPUT);
  
  if(!display.begin(SSD1306_SWITCHCAPVCC, 0x3C)) {
    Serial.println(F("OLED_INIT_FAIL"));
    for(;;); 
  }

  // --- AEGIS BOOT SEQUENCE ---
  display.clearDisplay();
  display.setTextSize(1);
  display.setTextColor(SSD1306_WHITE);
  display.setCursor(0,0);
  display.println(F("AEGIS KERNEL v4.0"));
  display.println(F("MOUNTING CRYPTO_VAULT..."));
  display.display();
  delay(1000);
}

void loop() {
  // 1. LAYER 1: PHYSICAL SIGNAL GENERATION
  int val = analogRead(potPin);
  // Safe: 1kHz (500us pulse) | Attack: 5kHz (100us pulse)
  int pulse = (val > 512) ? 500 : 100; 
  int currentHz = (val > 512) ? 1000 : 5000;

  for(int i = 0; i < 20; i++) {
    digitalWrite(signalOut, HIGH); delayMicroseconds(pulse);
    digitalWrite(signalOut, LOW);  delayMicroseconds(pulse);
  }

  // 2. LAYER 2: CRYPTOGRAPHIC DECISION READ
  bool isAuthorized = digitalRead(picoIn);

  // 3. TELEMETRY & UI REFRESH
  display.clearDisplay();
  
  // High-Tech Header
  display.fillRect(0, 0, 128, 10, SSD1306_WHITE);
  display.setCursor(2, 1);
  display.setTextColor(SSD1306_BLACK);
  display.print(F("AEGIS SECURITY CONSOLE"));
  display.setTextColor(SSD1306_WHITE);

  // Pilot Signal Data
  display.setCursor(0, 15);
  display.print(F("PILOT: ")); display.print(currentHz); display.print(F("Hz "));
  display.print((val > 512) ? F("[SAFE]") : F("[BREACH]"));

  // Status Visualization
  display.drawRect(5, 28, 118, 25, SSD1306_WHITE);
  if (isAuthorized) {
    digitalWrite(mosfetPin, HIGH);
    display.setCursor(32, 33);
    display.setTextSize(2);
    display.print(F("SECURE"));
    display.setTextSize(1);
    display.setCursor(0, 56);
    display.print(F("AUTH: 0xAF_VERIFIED"));
  } else {
    digitalWrite(mosfetPin, LOW);
    display.setCursor(24, 33);
    display.setTextSize(2);
    display.print(F("LOCKED!"));
    display.setTextSize(1);
    display.setCursor(0, 56);
    display.print(F("BLOCK: ILLEGAL_FREQ"));
  }
  
  display.display();
}
