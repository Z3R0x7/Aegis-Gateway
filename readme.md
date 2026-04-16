# Aegis Gateway: Cyber-Physical EV Firewall

This is the project I built for the **Make Mobility Challenge** final round. It’s a hardware-level firewall (Aegis Gateway) that sits between an Electric Vehicle (EV) and a charging station to stop cyber-physical attacks.

## The Idea
Most EV chargers use a basic signal to tell the car how much power to take. This signal isn't encrypted, so if a charging station gets hacked, it could send a "bad" signal to damage the car's electronics or force the charging lock to open. 

Aegis is a **Zero-Trust** bridge. It reads the signal on a Raspberry Pi Pico W, checks if the timing is correct, and only then passes it to the car. If it sees something weird, it physically cuts the connection.

---

## Hardware & Assembly

### 1. The Parts
I used a mix of microcontrollers for the simulation and industrial-grade components for the power switching.

![parts](./media/parts.jpg)
*Everything used: Arduino Uno (Attacker), RPi Pico W (Gateway), IRFZ44N MOSFET, and a 12V Solenoid.*

### 2. The Setup
Right now, the system is in the "Hardware-in-the-Loop" testing phase. The Arduino generates the PWM signal, the Pico analyzes it, and the Solenoid acts as the vehicle's physical lock.

![setup](./media/setup.jpg)
*The half-built system on the breadboard. You can see the logic bridge between the two microcontrollers.*

---

## How it Works
1. **The Attacker (Arduino Uno):** Mimics a compromised charger. I can change the PWM duty cycle using a knob (potentiometer) to test if the gateway catches the anomaly.
2. **The Gateway (RPi Pico W):** This is the brain. It runs at 133MHz, so it can react way faster than a software firewall. 
3. **The Switch (MOSFET):** A high-speed switch that handles the 12V power for the car's locking mechanism.

## Research Base
This project is based on the research paper: **"Exploiting and Securing the EV Charging Physical Layer"**. 
You can find the original paper here: [arXiv:2506.16400](https://arxiv.org/abs/2506.16400).

---

## Project Roadmap
- [ ] Add an OLED screen to show "Threat Levels" in real-time.
- [ ] Code a proper FFT (Fast Fourier Transform) to detect signal jitter.
- [ ] Design a 3D-printed case to make it look like a real product.

**Aegis is standing guard.** 🛡️⚡

```text
      (\_/)
      ( •_•)
      / >🛡️  "Access Denied!"