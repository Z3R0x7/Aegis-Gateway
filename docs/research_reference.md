# Research Context

This project is a physical implementation inspired by the research paper:
**"Exploiting and Securing the EV Charging Physical Layer"**
Link: [https://arxiv.org/abs/2506.16400](https://arxiv.org/abs/2506.16400)

### Key Takeaways Used:
1. **Physical Layer Vulnerability:** The Control Pilot (CP) signal is unencrypted and susceptible to manipulation.
2. **HIL Defense:** Implementing a Hardware-in-the-Loop (HIL) gateway can intercept malicious duty-cycle variations before they reach the vehicle's onboard charger (OBC).
3. **Zero-Trust Model:** The Aegis Gateway treats the charging station as an untrusted peripheral.