import os
from datetime import datetime

LOG_DIR = "logs"
VALID_LOG = os.path.join(LOG_DIR, "valid_streams.log")
BROKEN_LOG = os.path.join(LOG_DIR, "broken_streams.log")

def init_logs():
    """Log klasörünü ve dosyaları hazırlar"""
    os.makedirs(LOG_DIR, exist_ok=True)
    for path in [VALID_LOG, BROKEN_LOG]:
        if not os.path.exists(path):
            with open(path, "w", encoding="utf-8") as f:
                f.write(f"# Log created at {datetime.now()}\n")

def log_stream(name: str, url: str, status: bool):
    """Stream durumuna göre ilgili log dosyasına yazar"""
    log_line = f"{datetime.now()} | {'✅' if status else '❌'} | {name} | {url}\n"
    path = VALID_LOG if status else BROKEN_LOG
    with open(path, "a", encoding="utf-8") as f:
        f.write(log_line)

def count_broken_streams(threshold: int = 10) -> bool:
    """Hatalı stream sayısı eşik değerini geçiyor mu kontrol eder"""
    if not os.path.exists(BROKEN_LOG):
        return False
    with open(BROKEN_LOG, "r", encoding="utf-8") as f:
        lines = [line for line in f if line.strip() and not line.startswith("#")]
    return len(lines) >= threshold
