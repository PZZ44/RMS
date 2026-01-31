
import os

RISK_SERVICE_URL = os.getenv(
    "RISK_SERVICE_URL",
    "http://127.0.0.1:8000/risk/calculate"
)

BKI_URL = os.getenv(
    "BKI_URL",
    "http://127.0.0.1:8100/bki/score"
)

SIM_URL = os.getenv(
    "SIM_URL",
    "http://127.0.0.1:8200/sim/score"
)

RETRY_COUNT = int(os.getenv("RETRY_COUNT", 3)) #legacy
RETRY_DELAY = int(os.getenv("RETRY_DELAY", 1)) #legacy
REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", 3))
