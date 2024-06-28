#include <WiFi.h>
#include <ESPAsyncWebServer.h>
#include <Arduino.h>

const char* ssid = "MIWIFI_2G_usWV";
const char* password = "pZkKZ4GQ";

// Configuración de la IP estática
IPAddress local_IP(192, 168, 1, 100);      // IP que quieres asignar al ESP32
IPAddress gateway(192, 168, 1, 1);         // IP de la puerta de enlace
IPAddress subnet(255, 255, 255, 0);        // Máscara de subred
IPAddress primaryDNS(8, 8, 8, 8);          // Servidor DNS primario (opcional)
IPAddress secondaryDNS(8, 8, 4, 4);        // Servidor DNS secundario (opcional)

AsyncWebServer server(80);

// Función para generar valores simulados de corriente
float simulateCurrent() {
  // Genera un valor aleatorio de corriente basado en la potencia de una fuente de 650W
  float maxPower = 650.0f; // Potencia en vatios
  float efficiency = 0.85f; // Eficiencia de la fuente de alimentación
  float voltage = 230.0f; // Voltaje de salida
  float averagePower = maxPower * random(50, 75) / 100.0f; // Generar una corriente media alrededor del 50-75% del máximo
  float current =averagePower / (voltage * efficiency); // Corriente de entrada en amperios
  
  // Introduce una variación para simular condiciones reales usando una distribución normal
  float variation = static_cast<float>(random(-15, 15)) / 100.0f * current;
  return max(0.0f, current + variation); // Asegurarse de que la corriente no sea negativa

}

// Función que convierte la corriente simulada a consumo energético
float simulatePower(float current) {
  float voltage = 230.0f; // Voltaje de entrada AC
  float power = current * voltage * 0.85f; // Corriente multiplicada por el voltaje y eficiencia

  return min(power, 650.0f); // Limitar la potencia a un máximo de 650W
}

String getMetrics() {
    float current = simulateCurrent(); // Corriente simulada
    float power = simulatePower(current); // Potencia basada en la corriente simulada
    
    String metrics = "# HELP energy_current_amperes Current measured simulated in amperes\n";
    metrics += "# TYPE energy_current_amperes gauge\n";
    
    metrics += "energy_current_amperes{pin=\"simulated\"} " + String(current) + "\n";
    metrics += "# HELP energy_power_watts Power consumption in watts\n";
    metrics += "# TYPE energy_power_watts gauge\n";
    metrics += "energy_power_watts{pin=\"simulated\"} " + String(power) + "\n";
    Serial.print("---------------------------------");

    return metrics;
}

void setup() {
    Serial.begin(115200);
    WiFi.begin(ssid, password);

    // Conectar con IP estática
    if (!WiFi.config(local_IP, gateway, subnet, primaryDNS, secondaryDNS)) {
        Serial.println("Failed to configure STA");
    }

    while (WiFi.status() != WL_CONNECTED) {
        delay(1000);
        Serial.println("Connecting to WiFi...");
    }
    Serial.println("Connected to WiFi");
    Serial.print("IP Address: ");
    Serial.println(WiFi.localIP());

    server.on("/metrics", HTTP_GET, [](AsyncWebServerRequest *request){
        String metrics = getMetrics();
        request->send(200, "text/plain", metrics);
    });

    server.begin();
}

void loop() {
    // No es necesario manejar clientes de forma manual con AsyncWebServer
}

