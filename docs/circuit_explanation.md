# 🛠️ AEGIS — Circuit Explanation & Logic
This document provides a technical breakdown of the wiring and signal processing logic used in the AEGIS prototype. It is fully compliant with IEC 61851 Control Pilot signal specifications.

## 📍 Pin Mapping

### **Arduino Uno (Charger Simulator)**
| Pin | Role | Connected To |
| :--- | :--- | :--- |
| **A0** | Potentiometer Input | Potentiometer Wiper |
| **9** | PWM Signal Output | Pico GP0 (Physical Pin 1) |
| **2** | Gate Decision Input | Pico GP15 (Physical Pin 20) |
| **10** | MOSFET Control | MOSFET Gate Pin |
| **A4/A5** | I2C Communication | SSD1306 OLED SDA / SCL |

### **Raspberry Pi Pico W (Vehicle BMS)**
| Pin | Role | Connected To |
| :--- | :--- | :--- |
| **GP0** | PWM Signal Input | Arduino Pin 9 |
| **GP15** | Gate Decision Output | Arduino Pin 2 |
| **GND** | Common Ground | Arduino GND (Mandatory) |

---

## 📡 The Control Pilot Signal
The Control Pilot (CP) line carries the physical pulse that communicates the charging system status and max current. AEGIS audits this physical signal in real-time. The Pico monitors the incoming pulses from the Level Shifter using the `time_pulse_us()` function, with a $50\%$ duty cycle.

**Frequency Audit Logic:**
* **Legitimate ($1\text{kHz}$):** Total period is $1000\mu s$.
* **Malicious ($5\text{kHz}$):** Total period is $200\mu s$.

The Pico calculates the total period and defines a strict **"Safe Window" of $750\mu s$ to $1250\mu s$**. Any total period outside this window is immediately flagged as malicious, and the system **physically pulls Pin GP15 (the decision line) LOW**, overriding all other commands and initiating a total power cut.

---

## 🔐 Layer 2: Cryptographic Handshake
Once the physical signal is verified, the system proceeds to the Layer 2 security check. The protocol uses a robust **HMAC-SHA256 handshake** between the gateway (BMS) and the charger.

**Handshake Steps:**
1.  **Issue Challenge (Nonce):** The gateway (BMS) generates a dynamic, random numerical nonce.
2.  **Compute Response:** The charger terminal must sign this specific nonce using a shared **SECRET_KEY** to compute a single-use token.
3.  **Cross-Verify:** The gateway independently runs the same HMAC-SHA256 math and compares the tokens.

The output from the Pico looks like this:
> `PASSED | PWM PERIOD: 1002us (Legit) | Nonce: 64fa | Key Matched | GRANTED`

By utilizing a dynamic nonce, the key used for the current session is invalid for any future session, effectively neutralizing **Replay Attacks**. Power is only granted when the gate is physically asserted **HIGH** by the Pico on Pin GP15.

---

## ⚡ MOSFET Power Gating
The **IRF520 N-Channel MOSFET** module acts as the physical, logic-controlled gateway.
* **Active HIGH:** Current flows only when the Pico asserts the logic HIGH on Pin 2.
* **Fail-Safe LOW:** If the Pico detects any issue (Layer 1 or Layer 2 fail) or simply loses power, the decision pin falls to logic LOW. This cuts the physical connection between the vehicle and the power supply, prioritizing hardware safety.

![Circuit Schematic](../media/circ_dia.png)
