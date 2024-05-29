### Programbeskrivelse

Dette program styrer et smart låsesystem, der anvender forskellige sensorer og aktuatorer for at sikre adgang og overvågning. 
Programmet bruger MQTT-protokollen til kommunikation med en server, håndterer billedoptagelse og analyse, samt styrer en OLED-skærm og LED-indikatorer.

### Moduler og Funktioner

1. **paho.mqtt.client**: Bruges til MQTT-kommunikation, som muliggør publikation og modtagelse af beskeder mellem enheder.
2. **base64**: Bruges til at kode og dekode billeder til og fra base64-format.
3. **os**: Bruges til fil- og mappemanipulation.
4. **time**: Bruges til tidsstyring og forsinkelser.
5. **picamera**: Bruges til at tage billeder med Raspberry Pi-kameraet.
6. **DistanceSensor**: En brugerdefineret klasse til måling af afstand med en ultralydssensor.
7. **LedRGB**: En brugerdefineret klasse til styring af RGB LED-farver.
8. **rpi_ws281x**: Bruges til styring af RGB LED-strimler.
9. **ServoMotor**: En brugerdefineret klasse til styring af en servomotor.
10. **DoorSensor**: En brugerdefineret klasse til overvågning af dørstatus.
11. **SMBus**: Bruges til I2C-kommunikation med forskellige enheder.
12. **ssd1306**: Bruges til at styre en OLED-skærm.
13. **MosfetController**: En brugerdefineret klasse til at styre en solenoide via en MOSFET.

### Konfiguration

- **broker_address**: IP-adressen på MQTT-broker.
- **port**: Porten til MQTT-kommunikation.
- **topic_rasp**: MQTT-emnet til at sende billeder fra Raspberry Pi.
- **topic_server**: MQTT-emnet til at modtage genkendelsesresultater fra serveren.
- **image_folder**: Mappen hvor billeder gemmes.

### Funktioner og Flow

1. **on_connect**: Callback-funktion, der udføres ved oprettelse af forbindelse til MQTT-brokeren.
2. **on_message**: Callback-funktion, der udføres ved modtagelse af beskeder fra MQTT-brokeren.
3. **publish_image**: Funktion til at kode og publicere et billede til MQTT-brokeren.
4. **capture_images**: Funktion til at tage billeder med PiCamera og gemme dem i en mappe.
5. **measure_distance_loop**: Løkke der kontinuerligt måler afstand og styrer systemet baseret på afstandsdata.
6. **main**: Hovedfunktionen, der starter måleløkken.

### Applikationslogik

Programmet overvåger kontinuerligt afstand ved hjælp af en ultralydssensor. Når en person kommer tættere på, tager systemet billeder, 
der sendes til en server via MQTT. Serveren analyserer billederne og sender et svar tilbage. Baseret på svaret kan systemet give adgang ved at aktivere en solenoide og åbne en dør med en servomotor. 
OLED-skærmen viser statusmeddelelser, og LED-indikatorer bruges til at vise forskellige tilstande som tilladt adgang eller afvist adgang.
