# utils/validator.py
import re

class Validator:
    @staticmethod
    def email(email: str) -> bool:
        return bool(re.match(r"^[\w\.-]+@[\w\.-]+\.\w+$", email))

    @staticmethod
    def cpf(cpf: str) -> bool:
        return bool(re.match(r"^\d{11}$", cpf))

    @staticmethod
    def preco(valor: float) -> None:
        if valor <= 0:
            raise ValueError("O preço deve ser positivo.")
