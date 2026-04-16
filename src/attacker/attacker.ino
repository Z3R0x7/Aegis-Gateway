/* * Aegis Gateway - Attacker Simulation
 * Developed for Make Mobility Challenge
 * * Target: Arduino Uno
 * Goal: Generate a 1kHz PWM signal to simulate an EVSE Control Pilot.
 * A potentiometer on A0 allows for real-time manipulation of the signal.
 */

 const int potPin = A0; 
 const int outputPin = 9; // PWM Output to Gateway
 
 void setup() {
   pinMode(outputPin, OUTPUT);
   
   // Set Timer 1 for 1kHz PWM frequency
   // This mimics the standard EV charging communication frequency
   TCCR1B = (TCCR1B & 0b11111000) | 0x02; 
 }
 
 void loop() {
   int sensorValue = analogRead(potPin);
   
   // Map 0-1023 (pot) to 0-255 (PWM duty cycle)
   int dutyCycle = map(sensorValue, 0, 1023, 0, 255);
   
   analogWrite(outputPin, dutyCycle);
 }