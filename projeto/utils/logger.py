# utils/logger.py
from datetime import datetime
import os

# Classe responsável por registrar eventos do sistema (Separação de Preocupações)
class Logger:
    # Construtor: Garante que a pasta 'data/' existe e define o arquivo de log
    def __init__(self, log_file="data/log.txt"):
        os.makedirs(os.path.dirname(log_file), exist_ok=True)
        self.log_file = log_file

    # --- MÉTODOS PÚBLICOS DE LOG ---
    
    # Registra mensagens informativas
    def info(self, mensagem: str):
        self._write("INFO", mensagem)

    # Registra mensagens de erro (usado no tratamento de exceções)
    def error(self, mensagem: str):
        self._write("ERROR", mensagem)

    # --- MÉTODO PRIVADO DE ESCRITA ---
    
    # Método privado que formata e escreve a linha no arquivo
    def _write(self, nivel: str, mensagem: str):
        # Formata a linha com data/hora e nível (INFO ou ERROR)
        linha = f"{datetime.now().isoformat()} [{nivel}] {mensagem}\n"
        # Abre o arquivo em modo 'a' (append) para adicionar a linha no final
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(linha)