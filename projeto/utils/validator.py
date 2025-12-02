# utils/validator.py
import re

# Classe responsável por validar a integridade dos dados (Separação de Preocupações)
class Validator:
    
    # Método estático: Não precisa de uma instância da classe para ser chamado
    @staticmethod
    def email(email: str) -> bool:
        # Usa Expressão Regular (RegEx) para verificar o formato do e-mail
        return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))

    @staticmethod
    def cpf(cpf: str) -> bool:
        # Verifica se o CPF tem exatamente 11 dígitos numéricos
        return bool(re.match(r"^\d{11}$", cpf))

    @staticmethod
    def preco(valor: float) -> None:
        # Regra de Negócio: Garante que valores (preços) são sempre positivos
        if valor <= 0:
            raise ValueError("O preço deve ser positivo.")