# Evolutionary Cyber-Warfare Simulation (ECWS-MAS)

### 🛡️ Adaptive Zero-Day Exploit Detection & Patching using Multi-Agent Systems

This project is a sophisticated **Multi-Agent System (MAS)** simulation designed to model the adversarial dynamics of modern cyber warfare. It demonstrates how autonomous agents (Attacker vs. Defender) adapt to dynamic network changes, specifically focusing on the lifecycle of **Zero-Day Vulnerabilities**.

---

## 🚀 Key Features

* **Dynamic Network Topology:** The simulation environment changes in real-time, injecting new connections (edges) to simulate Zero-Day exploits.
* **Autonomous Agents:**
    * 🔴 **Red Agent (Attacker):** Uses **Q-Learning (RL)** to discover optimal attack paths and exploits autonomously without prior knowledge.
    * 🔵 **Blue Agent (Defender):** Uses **Game Theory & Statistical Analysis** to detect anomalies, deploy firewalls, and patch vulnerabilities dynamically.
* **Zero-Day Lifecycle Simulation:**
    1.  **Injection:** A new vulnerability is secretly added mid-simulation.
    2.  **Discovery:** The attacker finds and abuses the new path via simulated network scanning ("Knowledge Injection").
    3.  **Patching:** The defender observes the pattern and physically removes the path (Self-Healing Network).
* **Fog of War:** Implements Partial Observability; the attacker cannot see defenses until a collision occurs.
* **Tactical Retreat:** Advanced logic prevents the attacker from getting stuck in patched loops by forcing tactical fallbacks.

## 🛠️ Technologies Used

* **Python 3.x**
* **Tkinter** (GUI Visualization)
* **Reinforcement Learning** (Q-Learning Algorithm)
* **Multi-Agent Systems Theory**

## 📦 How to Run

1.  Clone the repository or download the ZIP file.
2.  Ensure Python is installed.
3.  Run the simulation:
    ```bash
    python gui.py
    ```

## 🎮 Simulation Scenario Guide

* **Rounds 1-3:** Attacker exploits a known vulnerability (Node 2).
* **Round 4:** Defender patches Node 2. Attacker struggles.
* **Round 7:** **NEW ZERO-DAY INJECTED (Node 1 -> 4).** Attacker discovers and exploits it immediately.
* **Round 11:** Defender detects and patches the Zero-Day.
* **Final Rounds:** System reaches a hardened state.

## 👨‍💻 Author

**Ali Alkhamees**
*Computer Science (AI) - Majmaah University*

---
*This project serves as a proof-of-concept for Adaptive Cyber Defense using AI.*
