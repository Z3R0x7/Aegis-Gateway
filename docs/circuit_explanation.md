# 🛠️ AEGIS — Circuit Explanation & Logic
This document provides a technical breakdown of the wiring and signal processing logic used in the AEGIS prototype.

## 📍 Pin Mapping

### **Arduino Uno (Charger Simulator)**
| Pin | Role | Connected To |
| :--- | :--- | :--- |
| **A0** | Potentiometer Input | Potentiometer Wiper |
| **9** | PWM Signal Output | Pico GP0 |
| **2** | Gate Decision Input | Pico GP15 |
| **10** | MOSFET Control | MOSFET Gate Pin |
| **A4/A5** | I2C Communication | OLED SDA / SCL |

### **Raspberry Pi Pico W (Vehicle BMS)**
| Pin | Role | Connected To |
| :--- | :--- | :--- |
| **GP0** | PWM Signal Input | Arduino Pin 9 |
| **GP15** | Gate Decision Output | Arduino Pin 2 |
| **GND** | Common Ground | Arduino GND (Mandatory) |

---

## 📡 The Control Pilot Signal
In compliance with **IEC 61851**, AEGIS monitors the Control Pilot (CP) line for frequency integrity. 

**Layer 1 Detection Logic:**
The Pico utilizes the `time_pulse_us()` function to measure the HIGH duration of the incoming pulse.
* **Normal ($1\text{kHz}$):** Pulse duration $\approx 500\mu s$ (Period $\approx 1000\mu s$).
* **Attack ($5\text{kHz}$):** Pulse duration $\approx 100\mu s$ (Period $\approx 200\mu s$).

> **Note:** If the period falls outside the $750\mu s$ to $1250\mu s$ tolerance window, the Pico immediately pulls **GP15 LOW**, overriding all other commands.

---

## 🔐 Layer 2: Cryptographic Handshake
Once the physical signal is validated, the system enters the challenge-response phase.

**The Math:**
The gateway and vehicle share a secret seed ($0xAF$). The validation follows this formula:
$$Key = (Nonce \oplus 0xAF) + 42$$

By using a dynamic **Nonce**, we ensure that even if an attacker sniffs the communication, the key used for the current session will be invalid for the next session, effectively neutralizing **Replay Attacks**.

---

## ⚡ MOSFET Power Gating
The **IRF520 MOSFET** acts as the final physical barrier. 
* **Active High:** Power only flows when the Pico confirms both layers are secure.
* **Fail-Safe:** If the Pico loses power or the code crashes, the Gate falls to **LOW**, physically disconnecting the vehicle from the charger.

![Circuit Schematic](../media/circuit_diagram.png)
