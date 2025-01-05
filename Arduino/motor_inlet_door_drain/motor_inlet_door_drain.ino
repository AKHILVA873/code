// CLK_HIGH_SPEED.ino or CLK_LOW_SPEED.ino

// Define the pins connected to the relays
const int relayPin0 = 6;
const int relayPin1 = 7;
const int relayPin2 = 8;
const int relayPin3 = 9;

const int door = 2;
const int inlet2 = 3;
const int inlet1 = 4;
const int drain = 5;




// Function prototypes
void chCommand();
void clCommand();
void ahCommand();
void alCommand();
void stCommand();
void inlet2HCommand();
void inlet2LCommand();
void inlet1HCommand();
void inlet1LCommand();
void drainHCommand();
void drainLCommand();
void doorHCommand();
void doorLCommand();

void setup() {
  // Initialize the relay pins as outputs
  pinMode(relayPin0, OUTPUT);
  pinMode(relayPin1, OUTPUT);
  pinMode(relayPin2, OUTPUT);
  pinMode(relayPin3, OUTPUT);


  pinMode(door, OUTPUT);
  pinMode(inlet2, OUTPUT);
  pinMode(inlet1, OUTPUT);
  pinMode(drain, OUTPUT);


  
  // Ensure the relays are initially off
  digitalWrite(relayPin0, LOW);
  digitalWrite(relayPin1, LOW);
  digitalWrite(relayPin2, LOW);
  digitalWrite(relayPin3, LOW);

  digitalWrite(door, HIGH);
  digitalWrite(inlet2, HIGH);
  digitalWrite(inlet1, HIGH);
  digitalWrite(drain, HIGH);
  Serial.begin(9600);
}









void loop() {
  // Check if data is available to read
  if (Serial.available() > 0) {
    // Read the incoming string
    String command = Serial.readStringUntil('\n');
    command.trim();  // Remove any trailing whitespace

    // Call corresponding functions based on the command
    if (command == "ch") {
      chCommand();
    } else if (command == "cl") {
      clCommand();
    } else if (command == "ah") {
      ahCommand();
    } else if (command == "al") {
      alCommand();
    } else if (command == "st") {
      stCommand();
    
    } else if (command == "inlet2H") {
      inlet2HCommand();
    } else if (command == "inlet2L") {
      inlet2LCommand();
    } else if (command == "inlet1H") {
      inlet1HCommand();
    } else if (command == "inlet1L") {
      inlet1LCommand();
    } else if (command == "drainH") {
      drainHCommand();
    } else if (command == "drainL") {
      drainLCommand();
    } else if (command == "doorH") {
      doorHCommand();
    } else if (command == "doorL") {
      doorLCommand();
    
    } else {
      Serial.println("Unknown command");
    }
  }
}

void chCommand() {
  // Add your code for ch command here
  Serial.println("clockwise High command received");
      //clock high
  digitalWrite(relayPin1, LOW);
  digitalWrite(relayPin2, LOW);
  digitalWrite(relayPin3, LOW);

  digitalWrite(relayPin0, HIGH);
}

void clCommand() {
  // Add your code for cl command here
  Serial.println("clockwise Low command received");
      // clock low
  digitalWrite(relayPin1, HIGH);
  digitalWrite(relayPin2, LOW);
  digitalWrite(relayPin3, LOW);

    digitalWrite(relayPin0, HIGH);
}

void ahCommand() {
  // Add your code for ah command here
  Serial.println("Anitclock High command received");
    //anti high
  digitalWrite(relayPin1, LOW);
  digitalWrite(relayPin2, HIGH);
  digitalWrite(relayPin3, HIGH);

    digitalWrite(relayPin0, HIGH);
}

void alCommand() {
  // Add your code for al command here
  Serial.println("Anticlock Low command received");
      // anti low
  digitalWrite(relayPin1, HIGH);
  digitalWrite(relayPin2, HIGH);
  digitalWrite(relayPin3, HIGH);

    digitalWrite(relayPin0, HIGH);
}

void stCommand() {
  // Add your code for st command here
  Serial.println("stop command received");
  digitalWrite(relayPin0,LOW);
  }


  

void inlet2HCommand() {
  // Add your code for st command here
  Serial.println("inlet valve 2 open");
  digitalWrite(inlet2,LOW);
  }

void inlet2LCommand() {
  // Add your code for st command here
  Serial.println("inlet valve 2 close");
  digitalWrite(inlet2,HIGH);
  }

void inlet1HCommand() {
  // Add your code for st command here
  Serial.println("inlet valve 1 open");
  digitalWrite(inlet1,LOW);
  }

void inlet1LCommand() {
  // Add your code for st command here
  Serial.println("inlet valve 1 close");
  digitalWrite(inlet1,HIGH);
  }


void drainHCommand() {
  // Add your code for st command here
  Serial.println("drain pump on");
  digitalWrite(drain,LOW);
  }


void drainLCommand() {
  // Add your code for st command here
  Serial.println("drain pump off");
  digitalWrite(drain,HIGH);
  }


void doorHCommand() {
  // Add your code for st command here
  Serial.println("door open");
  digitalWrite(door,LOW);
  }


void doorLCommand() {
  // Add your code for st command here
  Serial.println("door closed");
  digitalWrite(door,HIGH);
  }
