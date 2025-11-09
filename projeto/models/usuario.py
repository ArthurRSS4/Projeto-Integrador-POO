# models/usuario.py
from .pessoa import Pessoa

class Usuario(Pessoa):
    def __init__(self, id_pessoa: str, nome: str, email: str, cpf: str):
        super().__init__(id_pessoa, nome, email)
        self.cpf = cpf
        self.assinaturas = []  # composição: Usuario possui Assinaturas
        self.perfis = []       # composição: Usuario possui Perfis

    def papel(self) -> str:
        return "Usuario"

    def adicionar_perfil(self, perfil):
        self.perfis.append(perfil)

    def adicionar_assinatura(self, assinatura):
        self.assinaturas.append(assinatura)

    def to_dict(self) -> dict:
        base = super().to_dict()
        base.update({
            "cpf": self.cpf,
            "assinaturas": [a.to_dict() for a in self.assinaturas],
            "perfis": [p.to_dict() for p in self.perfis],
        })
        return base
