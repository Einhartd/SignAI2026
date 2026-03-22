#include <BLEDevice.h>
#include <BLEServer.h>
#include <BLE2902.h>

#define SERVICE_UUID "6E400001-B5A3-F393-E0A9-E50E24DCCA9E"
#define CHARACTERISTIC_UUID_TX "6E400003-B5A3-F393-E0A9-E50E24DCCA9E"

BLECharacteristic *pCharacteristic;
bool deviceConnected = false;

void setup() {
  Serial.begin(115200); 
  // UART2 do komunikacji z Nucleo (RX=16, TX=17)
  Serial2.begin(115200, SERIAL_8N1, 16, 17); 

  BLEDevice::init("SignAI_Gesture_Interface");
  BLEServer *pServer = BLEDevice::createServer();
  BLEService *pService = pServer->createService(SERVICE_UUID);
  pCharacteristic = pService->createCharacteristic(CHARACTERISTIC_UUID_TX, BLECharacteristic::PROPERTY_NOTIFY);
  pCharacteristic->addDescriptor(new BLE2902());
  pService->start();
  pServer->getAdvertising()->start();
  Serial.println("Gotowy na odbieranie gestów...");
}

void loop() {
  if (Serial2.available() > 0) {
    uint8_t gesture = Serial2.read();
    
    // Sprawdzamy czy to cyfra 0-7 lub błąd 'E'
    // if ((gesture >= '0' && gesture <= '7') && deviceConnected) {
      Serial.println(gesture);
      // Serial.println()
      pCharacteristic->setValue((uint8_t*)&gesture, 1);
      pCharacteristic->notify();
    // }
  }
}