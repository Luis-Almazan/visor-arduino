int leds[] = {2, 3, 4, 5, 6};  // Pines de los LEDs
int fingerCount = 0;
int prevCount = -1;

void setup() {
  Serial.begin(9600);
  // Configurar todos los LEDs como salidas
  for (int i = 0; i < 5; i++) {
    pinMode(leds[i], OUTPUT);
    digitalWrite(leds[i], LOW);  // Apagar todos al inicio
  }
  Serial.println("Sistema listo. Enviar numero de dedos desde Python.");
}

void loop() {
  if (Serial.available()) {
    fingerCount = Serial.parseInt();  // Leer número de dedos
    
    if (fingerCount != prevCount) {
      Serial.print("Dedos detectados: ");
      Serial.println(fingerCount);
      
      // Encender/Apagar LEDs según el conteo
      for (int i = 0; i < 5; i++) {
        digitalWrite(leds[i], (i < fingerCount) ? HIGH : LOW);
      }
      
      prevCount = fingerCount;
    }
  }
}