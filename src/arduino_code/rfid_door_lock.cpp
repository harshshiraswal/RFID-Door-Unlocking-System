/*
 * RFID DOOR UNLOCKING SYSTEM
 * College Mini Project - IoT Based Access Control
 * 
 * Description: Controls door lock using MFRC522 RFID reader
 * Features: RFID authentication, solenoid lock control, serial monitoring
 * 
 * Components:
 * - Arduino UNO
 * - MFRC522 RFID Reader
 * - Relay Module
 * - 12V Solenoid Lock
 * - 12V Power Supply
 * 
 * Connections:
 * RFID -> Arduino: SDA=10, SCK=13, MOSI=11, MISO=12, RST=9, 3.3V, GND
 * Relay -> Arduino: IN1=7, VCC=5V, GND=GND
 * Power -> Relay: JD-VCC=12V, COM=12V to Solenoid
 */

#include <SPI.h>
#include <MFRC522.h>

// =============================================================================
// PIN CONFIGURATION - Hardware connection definitions
// =============================================================================

#define RST_PIN     9     // Reset pin for RFID module
#define SS_PIN      10    // Slave Select pin for RFID module  
#define RELAY_PIN   7     // Control pin for relay module
#define BUZZER_PIN  6     // Optional: Buzzer for audio feedback
#define LED_GREEN   5     // Optional: Green LED for access granted
#define LED_RED     4     // Optional: Red LED for access denied

// =============================================================================
// RFID CONFIGURATION - Authorized card UIDs
// =============================================================================

// Create MFRC522 instance
MFRC522 mfrc522(SS_PIN, RST_PIN);

// Authorized RFID card UIDs - REPLACE THESE WITH YOUR ACTUAL CARD UIDs
// Format: {0xXX, 0xXX, 0xXX, 0xXX}
byte authorizedUID1[] = {0x12, 0x34, 0x56, 0x78};  // Replace with your first card
byte authorizedUID2[] = {0xAB, 0xCD, 0xEF, 0x01};  // Replace with your second card
byte authorizedUID3[] = {0x23, 0x45, 0x67, 0x89};  // Replace with your third card

// =============================================================================
// SYSTEM VARIABLES - Configuration parameters
// =============================================================================

const unsigned long UNLOCK_DURATION = 3000;  // Door unlock time in milliseconds (3 seconds)
const unsigned long BUZZER_BEEP = 200;       // Buzzer beep duration in milliseconds
const unsigned long DEBOUNCE_DELAY = 1000;   // Delay between card reads to prevent multiple triggers

// System state variables
bool systemActive = true;
unsigned long lastReadTime = 0;

// =============================================================================
// SETUP FUNCTION - Initializes system components
// =============================================================================

void setup() {
  // Initialize serial communication for monitoring and debugging
  Serial.begin(9600);
  Serial.println(F("================================================"));
  Serial.println(F("    RFID DOOR UNLOCKING SYSTEM"));
  Serial.println(F("    College Mini Project - IoT Access Control"));
  Serial.println(F("================================================"));
  Serial.println(F("Initializing system components..."));
  
  // Initialize SPI bus for RFID communication
  SPI.begin();
  
  // Initialize MFRC522 RFID reader
  mfrc522.PCD_Init();
  delay(4);  // Short delay for initialization
  
  // Initialize I/O pins
  pinMode(RELAY_PIN, OUTPUT);
  digitalWrite(RELAY_PIN, LOW);  // Ensure relay is OFF initially
  
  // Optional: Initialize LED and buzzer pins
  pinMode(LED_GREEN, OUTPUT);
  pinMode(LED_RED, OUTPUT);
  pinMode(BUZZER_PIN, OUTPUT);
  digitalWrite(LED_GREEN, LOW);
  digitalWrite(LED_RED, LOW);
  digitalWrite(BUZZER_PIN, LOW);
  
  // Display system information
  Serial.println(F("System Components:"));
  Serial.println(F("- MFRC522 RFID Reader"));
  Serial.println(F("- Relay Controlled Solenoid Lock"));
  Serial.println(F("- 12V DC Power System"));
  Serial.println();
  
  // Show RFID reader version
  Serial.print(F("RFID Reader: "));
  mfrc522.PCD_DumpVersionToSerial();
  
  Serial.println(F("System initialized successfully!"));
  Serial.println(F("Ready to scan RFID cards..."));
  Serial.println(F("================================================"));
  Serial.println();
}

// =============================================================================
// MAIN LOOP - Continuous system operation
// =============================================================================

void loop() {
  // Check if system is active
  if (!systemActive) {
    return;
  }
  
  // Prevent multiple rapid reads with debounce delay
  if (millis() - lastReadTime < DEBOUNCE_DELAY) {
    return;
  }
  
  // Look for new RFID cards
  if (!mfrc522.PICC_IsNewCardPresent()) {
    return;
  }
  
  // Select one of the cards
  if (!mfrc522.PICC_ReadCardSerial()) {
    return;
  }
  
  // Update last read time
  lastReadTime = millis();
  
  // Process the scanned card
  processRFIDCard();
  
  // Halt PICC (Proximity Integrated Circuit Card) to prepare for next read
  mfrc522.PICC_HaltA();
}

// =============================================================================
// CARD PROCESSING FUNCTIONS
// =============================================================================

void processRFIDCard() {
  // Display card information
  displayCardInfo();
  
  // Check if the card is authorized
  if (isAuthorizedCard()) {
    grantAccess();
  } else {
    denyAccess();
  }
}

void displayCardInfo() {
  Serial.println(F("----------------------------------------"));
  Serial.print(F("RFID Card Detected - UID: "));
  
  // Display UID in hexadecimal format
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
    Serial.print(mfrc522.uid.uidByte[i], HEX);
  }
  Serial.println();
  
  // Display UID in decimal format
  Serial.print(F("UID (Decimal): "));
  for (byte i = 0; i < mfrc522.uid.size; i++) {
    Serial.print(mfrc522.uid.uidByte[i]);
    if (i < mfrc522.uid.size - 1) Serial.print(", ");
  }
  Serial.println();
}

// =============================================================================
// ACCESS CONTROL FUNCTIONS
// =============================================================================

bool isAuthorizedCard() {
  // Compare scanned UID with all authorized UIDs
  if (compareUID(mfrc522.uid.uidByte, authorizedUID1, mfrc522.uid.size)) {
    Serial.println(F("✓ Authorized Card 1 Recognized"));
    return true;
  }
  
  if (compareUID(mfrc522.uid.uidByte, authorizedUID2, mfrc522.uid.size)) {
    Serial.println(F("✓ Authorized Card 2 Recognized"));
    return true;
  }
  
  if (compareUID(mfrc522.uid.uidByte, authorizedUID3, mfrc522.uid.size)) {
    Serial.println(F("✓ Authorized Card 3 Recognized"));
    return true;
  }
  
  return false;
}

bool compareUID(byte* scannedUID, byte* authorizedUID, byte size) {
  for (byte i = 0; i < size; i++) {
    if (scannedUID[i] != authorizedUID[i]) {
      return false;
    }
  }
  return true;
}

// =============================================================================
// ACCESS GRANTED SEQUENCE
// =============================================================================

void grantAccess() {
  Serial.println(F("✅ ACCESS GRANTED - Door Unlocking!"));
  
  // Visual and audio feedback
  indicateAccessGranted();
  
  // Activate relay to unlock door
  unlockDoor();
  
  // Wait while door is unlocked
  delay(UNLOCK_DURATION);
  
  // Deactivate relay to lock door
  lockDoor();
  
  Serial.println(F("🔒 Door Locked - Ready for next scan"));
  Serial.println(F("----------------------------------------"));
  Serial.println();
}

void indicateAccessGranted() {
  // Green LED ON
  digitalWrite(LED_GREEN, HIGH);
  digitalWrite(LED_RED, LOW);
  
  // Success beep pattern
  beep(BUZZER_PIN, BUZZER_BEEP);
  delay(100);
  beep(BUZZER_PIN, BUZZER_BEEP);
}

void unlockDoor() {
  digitalWrite(RELAY_PIN, HIGH);  // Activate relay
  Serial.println(F("🔓 Relay Activated - Solenoid Unlocked"));
  Serial.println(F("⏰ Unlock duration: 3 seconds"));
}

void lockDoor() {
  digitalWrite(RELAY_PIN, LOW);   // Deactivate relay
  digitalWrite(LED_GREEN, LOW);   // Turn off green LED
  Serial.println(F("🔒 Relay Deactivated - Solenoid Locked"));
}

// =============================================================================
// ACCESS DENIED SEQUENCE
// =============================================================================

void denyAccess() {
  Serial.println(F("❌ ACCESS DENIED - Unauthorized Card!"));
  
  // Visual and audio feedback
  indicateAccessDenied();
  
  Serial.println(F("⚠️  Please use authorized RFID card"));
  Serial.println(F("----------------------------------------"));
  Serial.println();
}

void indicateAccessDenied() {
  // Red LED ON
  digitalWrite(LED_RED, HIGH);
  digitalWrite(LED_GREEN, LOW);
  
  // Error beep pattern
  for (int i = 0; i < 3; i++) {
    beep(BUZZER_PIN, BUZZER_BEEP);
    delay(300);
  }
  
  // Turn off red LED after indication
  delay(1000);
  digitalWrite(LED_RED, LOW);
}

// =============================================================================
// UTILITY FUNCTIONS
// =============================================================================

void beep(int pin, unsigned long duration) {
  digitalWrite(pin, HIGH);
  delay(duration);
  digitalWrite(pin, LOW);
}

// =============================================================================
// SERIAL COMMAND INTERFACE (Optional - for advanced control)
// =============================================================================

void serialEvent() {
  while (Serial.available()) {
    String command = Serial.readStringUntil('\n');
    command.trim();
    
    if (command == "STATUS") {
      Serial.println(F("=== SYSTEM STATUS ==="));
      Serial.println(F("RFID Door Unlock System - ACTIVE"));
      Serial.println(F("Ready to scan authorized cards"));
      Serial.println(F("====================="));
    }
    else if (command == "RESET") {
      Serial.println(F("System reset initiated..."));
      setup();
    }
    else if (command == "HELP") {
      displayHelp();
    }
  }
}

void displayHelp() {
  Serial.println(F("=== SERIAL COMMANDS ==="));
  Serial.println(F("STATUS - Display system status"));
  Serial.println(F("RESET  - Reset the system"));
  Serial.println(F("HELP   - Show this help message"));
  Serial.println(F("======================="));
}

/*
 * TROUBLESHOOTING NOTES:
 * 
 * 1. If RFID reader is not detected:
 *    - Check SPI connections (SDA, SCK, MOSI, MISO)
 *    - Verify 3.3V power to RFID module
 *    - Ensure proper grounding
 * 
 * 2. If relay is not activating:
 *    - Check 12V power supply to JD-VCC
 *    - Verify relay control pin connection
 *    - Test relay with manual input
 * 
 * 3. To add new authorized cards:
 *    - Scan the card and note the UID from Serial Monitor
 *    - Replace the UID arrays with your actual card UIDs
 *    - Upload the modified code
 * 
 * 4. Serial Monitor should show:
 *    - Card UID when scanned
 *    - Access granted/denied messages
 *    - System status information
 */

/*
 * PROJECT FEATURES DEMONSTRATED:
 * 
 * ✅ RFID Technology Integration
 * ✅ Secure Access Control System
 * ✅ Hardware Interfacing (Relay, Solenoid)
 * ✅ Serial Communication & Monitoring
 * ✅ Error Handling & User Feedback
 * ✅ Modular Code Structure
 * ✅ Professional Documentation
 * ✅ Real-world IoT Application
 */