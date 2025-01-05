#define DOUT 4
#define PD_SCK 3
#define DIGITAL_PIN 2  // Define the digital pin
#define ANALOG_PIN A0  // Define the analog pin

long readCount() {
  long count = 0;
  pinMode(DOUT, INPUT);

  while (digitalRead(DOUT));  // wait for DOUT to go low

  for (int i = 0; i < 24; i++) {
    digitalWrite(PD_SCK, HIGH);
    delayMicroseconds(1);
    count = count << 1;
    digitalWrite(PD_SCK, LOW);
    if (digitalRead(DOUT)) {
      count++;
    }
  }

  // Set the channel and gain factor (128 or 64)
  digitalWrite(PD_SCK, HIGH);
  count = count ^ 0x800000;  // 24th pulse
  delayMicroseconds(1);
  digitalWrite(PD_SCK, LOW);

  return count;
}

void setup() {
  Serial.begin(9600);
  pinMode(PD_SCK, OUTPUT);
  pinMode(DOUT, INPUT);    // Set DOUT as input for the HX711
  pinMode(DIGITAL_PIN, INPUT);  // Set digital pin 2 as input
  pinMode(ANALOG_PIN, INPUT);  // Set analog pin A0 as input
}

void loop() {
  long count = readCount();
  float voltage = (float)count / 16777216.0 * 5.0;  // Convert count to voltage

  // Assuming the pressure sensor's voltage output is proportional to water depth
  float waterLevel = voltage * 10.0;  // Example conversion factor, adjust as needed
  Serial.print("watersensor: ");
  Serial.print(voltage, 3);
  Serial.println("");

  // Read analog pin A0
  int analogValue = analogRead(ANALOG_PIN);
  Serial.print("taccosensor: ");
  Serial.println(analogValue);

  // Read digital pin 2
  int digitalValue = digitalRead(DIGITAL_PIN);
  Serial.print("doorssensor: ");
  Serial.println(digitalValue);

  delay(500);
}
