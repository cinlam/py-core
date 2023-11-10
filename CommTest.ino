#include <SPI.h>
#include <Wire.h>

#define VCP_MONITOR_ADDRESS 0xFE
#define MANUFACTURER_ID_REG 0xFE
#define SS_PIN 53 // Slave Select (SS) pin for SPI communication

// Declare arrays for each communication protocol
const int MAX_SERIAL_DATA_SIZE = 3; // Maximum number of bytes for serial data
uint8_t serialData[MAX_SERIAL_DATA_SIZE];
const int MAX_SPI_DATA_SIZE = 3; // Maximum number of bytes for SPI data
uint8_t spiData[MAX_SPI_DATA_SIZE];
const int MAX_I2C_DATA_SIZE = 3; // Maximum number of bytes for I2C data
uint8_t i2cData[MAX_I2C_DATA_SIZE];

// Declare indices for each array
volatile int serialDataIndex = 0;
volatile int spiDataIndex = 0;
volatile int i2cDataIndex = 0;

const byte interruptPin = 2;
volatile bool dataStarted = false;

// Definition of states
enum State {
    NoOperation,
    UART_CRC_Calc,
    SPI_CRC_Calc,
    I2C_CRC_Calc,
    Parse
};

// Variable to store the current state
State currentState;

void setup() {
    // Initialization
    currentState = NoOperation;

    Serial.begin(9600);
    Serial1.begin(9600); // Initialize UART on pins 0 and 1
    SPI.begin();
    Wire.begin();
    pinMode(SS_PIN, OUTPUT);
    digitalWrite(SS_PIN, HIGH); // Deselect the SPI slave
    pinMode(interruptPin, INPUT_PULLUP);
    attachInterrupt(digitalPinToInterrupt(interruptPin), handleInterrupt, RISING);
}

uint16_t calculate_crc(uint8_t *data, size_t length) {
    uint16_t calculated_crc = 0xFFFF; // Initial value of CRC

    for (size_t i = 0; i < length; i++) {
        calculated_crc ^= data[i];

        for (uint8_t j = 0; j < 8; j++) {
            if (calculated_crc & 0x0001) {
                calculated_crc = (calculated_crc >> 1) ^ 0xA001; // XOR with polynomial
            } else {
                calculated_crc >>= 1;
            }
        }
    }

    return calculated_crc;
}

void processUARTCommunication() {
    uint8_t response[3]; // Assuming 5 bytes of response data

    // Populate the response data with the appropriate values
    response[0] = 0x46; // Example modification: Increment the first byte value by 1
    response[1] = 0x8B; // Example modification: Increment the second byte value by 2
    response[2] = 0x78; // Example modification: Increment the third byte value by 3

    // Calculate the CRC-16 for the response data
    uint16_t calculated_crc = calculate_crc(response, sizeof(response));

    // Send the response data and CRC back via UART
    for (int i = 0; i < sizeof(response); i++) {
        Serial1.write(response[i]);
    }
    Serial1.write(calculated_crc >> 8); // High byte of CRC
    Serial1.write(calculated_crc & 0xFF); // Low byte of CRC
}

void processSPICommunication() {
    digitalWrite(SS_PIN, LOW); // Select the SPI slave

    uint8_t response[3]; // Assuming 3 bytes of response data

    // Populate the response data with the appropriate values
    response[0] = 0x01; // Example value for the first byte
    response[1] = 0x02; // Example value for the second byte
    response[2] = 0x03; // Example value for the third byte

    // Calculate the CRC-16 for the response data
    uint16_t calculated_crc = calculate_crc(response, sizeof(response));

    // Send the response data and CRC back via SPI
    for (int i = 0; i < sizeof(response); i++) {
        SPI.transfer(response[i]);
    }
    SPI.transfer(calculated_crc >> 8); // High byte of CRC
    SPI.transfer(calculated_crc & 0xFF); // Low byte of CRC

    digitalWrite(SS_PIN, HIGH); // Deselect the SPI slave
}

void processI2CCommunication() {
    uint8_t response[2];
    response[0] = VCP_MONITOR_ADDRESS;
    response[1] = 0x00;
    Wire.beginTransmission(VCP_MONITOR_ADDRESS);
    Wire.write(response, sizeof(response));
    Wire.endTransmission();
    delay(1); // Wait for the device to process the data
}

void loop() {
    if (dataStarted) {
        switch (currentState) {
            case NoOperation:
                if (serialDataIndex == MAX_SERIAL_DATA_SIZE)
                    currentState = UART_CRC_Calc;
                else if (spiDataIndex == MAX_SPI_DATA_SIZE)
                    currentState = SPI_CRC_Calc;
                else if (i2cDataIndex == MAX_I2C_DATA_SIZE)
                    currentState = I2C_CRC_Calc;
                break;

            case UART_CRC_Calc:
            case SPI_CRC_Calc:
            case I2C_CRC_Calc: {
                uint8_t* data;
                const int dataSize = (currentState == UART_CRC_Calc) ? MAX_SERIAL_DATA_SIZE :
                                      (currentState == SPI_CRC_Calc) ? MAX_SPI_DATA_SIZE :
                                      MAX_I2C_DATA_SIZE;

                if (currentState == UART_CRC_Calc)
                    data = serialData;
                else if (currentState == SPI_CRC_Calc)
                    data = spiData;
                else
                    data = i2cData;

                uint16_t received_crc = (data[dataSize - 2] << 8) | data[dataSize - 1];
                uint16_t calculated_crc = calculate_crc(data, dataSize - 2);

                if (received_crc == calculated_crc)
                    Serial.println((currentState == UART_CRC_Calc) ? "UART: CRC-16 verification successful. No errors detected." :
                                   (currentState == SPI_CRC_Calc) ? "SPI: CRC-16 verification successful. No errors detected." :
                                   "I2C: CRC-16 verification successful. No errors detected.");
                else
                    Serial.println((currentState == UART_CRC_Calc) ? "UART: CRC-16 verification failed. Errors detected in the received data." :
                                   (currentState == SPI_CRC_Calc) ? "SPI: CRC-16 verification failed. Errors detected in the received data." :
                                   "I2C: CRC-16 verification failed. Errors detected in the received data.");

                currentState = Parse;

                // Reset data indices
                serialDataIndex = 0;
                spiDataIndex = 0;
                i2cDataIndex = 0;

                break;
            }

            case Parse:
                // Process the received data
                // TODO Add code to handle the received data in the Parse state
                break;
        }
    }

    processUARTCommunication();
    processSPICommunication();
    processI2CCommunication();
}

void handleInterrupt() {
    if (Serial.available()) {
        // Capture serial data
        if (serialDataIndex < MAX_SERIAL_DATA_SIZE) {
            serialData[serialDataIndex] = Serial.read();
            serialDataIndex++;
        }
    }

    if (digitalRead(SS_PIN) == LOW) {
        // Capture SPI data
        if (spiDataIndex < MAX_SPI_DATA_SIZE) {
            spiData[spiDataIndex] = SPI.transfer(0);
            spiDataIndex++;
        }
    }

    if (Wire.available()) {
        // Capture I2C data
        if (i2cDataIndex < MAX_I2C_DATA_SIZE) {
            i2cData[i2cDataIndex] = Wire.read();
            i2cDataIndex++;
        }
    }

    // Update flags or trigger quick actions if necessary
    dataStarted = true;
}
