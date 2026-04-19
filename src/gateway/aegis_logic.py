 from machine import Pin, time_pulse_us
import time

audit_in = Pin(0, Pin.IN)
trigger_out = Pin(15, Pin.OUT) # Physical Pin 20

TARGET_PERIOD = 1000 
TOLERANCE = 250

print("--- PICO AUDITOR STARTING ---")



while True:
    duration = time_pulse_us(audit_in, 1, 100000)
    period = duration * 2 if duration > 0 else 0
    
    if period > 0:
        if (TARGET_PERIOD - TOLERANCE) < period < (TARGET_PERIOD + TOLERANCE):
            print(f"SAFE SIGNAL DETECTED: {period}us")
            trigger_out.value(1) # Send HIGH to Arduino
        else:
            print(f"ATTACK DETECTED: {period}us")
            trigger_out.value(0) # Send LOW to Arduino
    else:
        print("NO SIGNAL DETECTED")
        trigger_out.value(0)
        
    time.sleep(0.1)

