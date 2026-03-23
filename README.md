# SpatialKey
**SignAI 2026 Hackathon Project**

## Overview

SpatialKey is a hardware-software solution developed within a 24-hour timeframe during the SignAI 2026 hackathon. The system leverages a Time-of-Flight (ToF) sensor and Edge AI processing to recognize static hand gestures and transmit them via Bluetooth Low Energy (BLE) to a personal computer, where they are translated into dynamic system commands.

## Key Features

* **Edge AI Gesture Recognition:** Utilizes on-device machine learning models to process sensor data and accurately classify static hand postures with minimal latency.
* **Wireless Communication:** Establishes an automated connection to the host machine via BLE (identifying as the `ESP32_Button_Sender` device).
* **Dynamic Macro Execution:** Translates incoming gesture classifications directly into operating system-level media controls and mouse actions.
* **Graphical User Interface:** Includes a desktop application that provides real-time connection status, current gesture visualization, and a command execution history.

## Default Gesture Mapping

The application is configured to recognize a specific set of hand postures, mapping them to the following automated actions:

* **FLAT_HAND:** Media Play / Pause
* **LIKE:** System Volume Up
* **DISLIKE:** System Volume Down
* **FIST:** Next Media Track
* **LOVE:** Previous Media Track
* **BREAKTIME:** Left Mouse Click
* **CROSSHANDS:** Mouse Scroll Up

## Technology Stack

**Hardware & Embedded Systems:**
* Time-of-Flight (ToF) Sensor (VL53L8CX)
* Microcontroller (STM32 series)
* BLE Communication Module

**PC Application (Python):**
* `bleak` - Asynchronous Bluetooth Low Energy client operations.
* `pynput` - Cross-platform control of virtual input devices (keyboard and mouse).
* `Tkinter` - Application GUI framework.

## Team Members
- [Oliwier Kniażewski](https://github.com/Einhartd)
- [Piotr Sawicki](https://github.com/Piotreksaw)
- [Michał Piotrkowski](https://github.com/mich4elo)
- [Mateusz Połubiński](https://github.com/mateuszpolubinski1)
