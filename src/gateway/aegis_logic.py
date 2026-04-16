# Aegis Gateway - Security Logic
# Running on MicroPython (RPi Pico W)

from machine import Pin
import time

# Pin Definitions
attacker_in = Pin(0, Pin.IN)  # Input signal from Arduino
car_out = Pin(1, Pin.OUT)     # Filtered output to MOSFET/Solenoid

print("--- Aegis Gateway Active ---")
print("Monitoring physical layer for anomalies...")

while True:
    # Baseline Pass-Through Logic
    # This acts as a high-speed logic bridge. 
    # Future updates will include frequency analysis and jitter detection.
    
    if attacker_in.value() == 1:
        car_out.value(1)
    else:
        car_out.value(0)