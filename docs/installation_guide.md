# Installation Guide

## Hardware Requirements

### Components Needed:
- Arduino UNO R3
- MFRC522 RFID Reader Module
- 2-Channel Relay Module
- 12V Solenoid Lock
- 12V 2A DC Power Supply
- RFID Cards/Tags
- Jumper Wires
- Breadboard (optional)

### Tools Required:
- USB Cable for Arduino
- Screwdriver
- Wire Strippers
- Multimeter (for verification)

## Step-by-Step Installation

### 1. Hardware Assembly

#### Power Connections:
1. Connect 12V DC power supply to relay module JD-VCC
2. Connect 12V DC positive to solenoid lock
3. Connect common ground for all components

#### Arduino to RFID:
- SDA → Digital 10
- SCK → Digital 13  
- MOSI → Digital 11
- MISO → Digital 12
- RST → Digital 9
- 3.3V → 3.3V
- GND → GND

#### Arduino to Relay:
- IN1 → Digital 7
- VCC → 5V
- GND → GND

### 2. Software Setup

#### Arduino IDE Setup:
1. Download and install Arduino IDE
2. Install MFRC522 library:
   - Go to Sketch → Include Library → Manage Libraries
   - Search for "MFRC522" and install

#### Upload Code:
1. Connect Arduino via USB
2. Open `src/arduino_code/rfid_door_lock.ino`
3. Select correct board (Arduino UNO) and port
4. Click Upload

### 3. Testing & Calibration

#### Initial Test:
1. Open Serial Monitor (9600 baud)
2. Scan an RFID card
3. Check if UID is displayed
4. Modify authorized UIDs in code with your cards

#### Safety Checks:
- Verify all connections before powering
- Check voltage levels with multimeter
- Ensure proper isolation between power domains

## Troubleshooting

### Common Issues:

1. **RFID not detected**
   - Check SPI connections
   - Verify 3.3V power to RFID module
   - Ensure proper grounding

2. **Relay not activating**
   - Check 12V power supply
   - Verify JD-VCC connection
   - Test relay with manual input

3. **Solenoid not working**
   - Verify 12V power to solenoid
   - Check relay output connections
   - Test solenoid directly with power supply

### Serial Monitor Output:
- Successful read: "Card UID: XX XX XX XX"
- Authorized: "ACCESS GRANTED - Door Unlocked!"
- Unauthorized: "ACCESS DENIED - Unauthorized Card!"