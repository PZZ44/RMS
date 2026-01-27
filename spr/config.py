"""
Конфигурация SPR (Decision Service)

Здесь хранятся:
- URL внешних сервисов
- базовые сетевые таймауты

ВАЖНО:
- никакой бизнес-логики здесь быть не должно
- значения могут переопределяться через ENV
"""

import os

# === Risk Service ===
# Сервис внутреннего риска (возраст, лояльность, история)
RISK_SERVICE_URL = os.getenv(
    "RISK_SERVICE_URL",
    "http://127.0.0.1:8000/risk/calculate"
)

# === BKI ===
# Эмуляция бюро кредитных историй
BKI_URL = os.getenv(
    "BKI_URL",
    "http://127.0.0.1:8100/bki/score"
)

# === SIM ===
# Эмуляция телеком-скора
SIM_URL = os.getenv(
    "SIM_URL",
    "http://127.0.0.1:8200/sim/score"
)

# Таймаут на HTTP-запросы (сек)
RETRY_COUNT = int(os.getenv("RETRY_COUNT", 3)) #legacy
RETRY_DELAY = int(os.getenv("RETRY_DELAY", 1)) #legacy
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 3))
