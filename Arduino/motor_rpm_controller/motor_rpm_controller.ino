const int triacPulse = 10;  
const int inputPin = 2;
int delayValue = 7000;  // Default delay value

void setup() {
  pinMode(triacPulse, OUTPUT);  // Set the MOC3021 pin as output
  pinMode(inputPin, INPUT);     // Set the input pin to read sensor values
  Serial.begin(9600);           // Start serial communication at 9600 baud
  Serial.println("Enter delay value in microseconds:");
}

void loop() {
  // Check if there is serial input available
  if (Serial.available() > 0) {
    // Read the input as a string
    String input = Serial.readStringUntil('\n');
    // Convert the input to an integer
    delayValue = input.toInt();
    Serial.print("New delay value set to: ");
    Serial.println(delayValue);
  }

  int sensorValue = digitalRead(inputPin);  // Read the state of the input pin

  if (sensorValue == HIGH) {
    digitalWrite(triacPulse, LOW);   // Set the triacPulse pin HIGH
    delayMicroseconds(delayValue);    // Wait for the specified microseconds
    digitalWrite(triacPulse, HIGH);
  }
}
