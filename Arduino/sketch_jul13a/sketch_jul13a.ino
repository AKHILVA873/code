void setup() {
  // Start the serial communication
  Serial.begin(9600);
}

void loop() {
  // Loop from 0 to 100
  for (int counter = 0; counter <= 100; counter++) {
    // Print the counter value to the Serial Monitor
    Serial.println(counter);
    // Add a small delay to make the output readable
    delay(100);
  }
}
