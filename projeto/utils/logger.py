# utils/logger.py
from datetime import datetime
import os

class Logger:
    def __init__(self, log_file="data/log.txt"):
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        self.log_file = log_file

    def info(self, mensagem: str):
        self._write("INFO", mensagem)

    def error(self, mensagem: str):
        self._write("ERROR", mensagem)

    def _write(self, nivel: str, mensagem: str):
        linha = f"{datetime.now().isoformat()} [{nivel}] {mensagem}\n"
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(linha)
