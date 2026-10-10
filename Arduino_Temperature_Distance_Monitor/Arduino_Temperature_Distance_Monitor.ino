#include <Adafruit_LiquidCrystal.h>

// Initializam LCD-ul
Adafruit_LiquidCrystal lcd(0);

// Pinul pentru senzorul de temperatura
#define TEMP_PIN A0

// Pinii pentru senzorul ultrasonic
#define TRIG_PIN 9
#define ECHO_PIN 10

void setup() {
  // Pornim LCD-ul cu 16 coloane si 2 randuri
  lcd.begin(16, 2);
  lcd.setBacklight(1);

  // TRIG trimite semnalul, ECHO primeste raspunsul
  pinMode(TRIG_PIN, OUTPUT);
  pinMode(ECHO_PIN, INPUT);

  // Mesaj scurt la pornirea proiectului
  lcd.setCursor(0, 0);
  lcd.print("Starting...");
  delay(1000);
}

void loop() {
  // Citim valoarea de la senzorul de temperatura
  int sensorValue = analogRead(TEMP_PIN);

  // Transformam valoarea citita in tensiune
  float voltage = sensorValue * (5.0 / 1023.0);

  // TMP36 da 0.5V la 0 grade C, apoi 10mV pentru fiecare grad
  float temperature = (voltage - 0.5) * 100.0;

  // Pregatim senzorul ultrasonic pentru masurare
  digitalWrite(TRIG_PIN, LOW);
  delayMicroseconds(2);

  // Trimitem un impuls scurt pe TRIG
  digitalWrite(TRIG_PIN, HIGH);
  delayMicroseconds(10);
  digitalWrite(TRIG_PIN, LOW);

  // Masuram cat timp sta semnalul pe HIGH pe pinul ECHO
  long duration = pulseIn(ECHO_PIN, HIGH);

  // Calculam distanta in cm
  // 0.0343 cm/us este viteza sunetului, iar impartim la 2 pentru dus-intors
  float distance = duration * 0.0343 / 2;

  // Curatam LCD-ul si afisam valorile noi
  lcd.clear();

  // Afisam temperatura pe primul rand
  lcd.setCursor(0, 0);
  lcd.print("Temp:");
  lcd.print(temperature, 1);
  lcd.print(" C");

  // Afisam distanta pe al doilea rand
  lcd.setCursor(0, 1);
  lcd.print("Dist:");
  lcd.print(distance, 0);
  lcd.print(" cm");

  // Asteptam o secunda pana la urmatoarea citire
  delay(1000);
}
