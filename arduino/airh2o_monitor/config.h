#ifndef CONFIG_H
#define CONFIG_H

#include <Arduino.h>

// ===== Wi-Fi =====
#define WIFI_SSID "PEDRO"
#define WIFI_PASSWORD "salvador"

// ===== Identificacao deste dispositivo no banco =====
#define DISPOSITIVO_ID "esp32-reservatorio-01"
#define DISPOSITIVO_NOME "Reservatório Principal - ETEC"

// ===== API =====

#define API_BASE_URL "http://192.168.137.1:8000"
#define API_MEDICOES_PATH "/api/medicoes"

// ===== Tempos =====
#define INTERVALO_LEITURA_MS 50       // le os sensores a cada 50 ms
#define DEBOUNCE_MS 300               // nivel precisa ficar estavel 300 ms antes de enviar
#define INTERVALO_HEARTBEAT_MS 30000  // reenvia o nivel atual a cada 30 s, mesmo sem mudanca
#define INTERVALO_RETRY_MS 2000       // se o envio falhar, tenta de novo a cada 2 s
#define INTERVALO_RECONEXAO_MS 10000  // espera apos falha de Wi-Fi

// ===== Reservatorio =====
#define CAPACIDADE_LITROS 500.0f

// ===== Pinos (ESP32-WROOM-32) =====

static const uint8_t PIN_SENSOR_NIVEL_25 = 25;  // 25%
static const uint8_t PIN_SENSOR_NIVEL_50 = 26;  // 50%
static const uint8_t PIN_SENSOR_NIVEL_75 = 27;  // 75%
static const uint8_t PIN_SENSOR_NIVEL_100 = 14; // 100%

// ===== HTTP =====
#define HTTP_MAX_TENTATIVAS 1
#define HTTP_TIMEOUT_MS 3000

#endif
