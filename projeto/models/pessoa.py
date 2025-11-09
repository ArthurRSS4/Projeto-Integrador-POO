# models/pessoa.py
from abc import ABC, abstractmethod

class Pessoa(ABC):
    def __init__(self, id_pessoa: str, nome: str, email: str):
        self.id_pessoa = id_pessoa
        self.nome = nome
        self.email = email

    @abstractmethod
    def papel(self) -> str:
        """Retorna o papel da pessoa no sistema."""
        pass

    def to_dict(self) -> dict:
        return {
            "id_pessoa": self.id_pessoa,
            "nome": self.nome,
            "email": self.email,
            "papel": self.papel()
        }
