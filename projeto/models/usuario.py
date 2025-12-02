# models/usuario.py
from .pessoa import Pessoa # <--- LINHA CORRIGIDA: Importa a classe Pessoa
from datetime import date # Assumindo que Pessoa usa date ou você usa em Usuario

class Usuario(Pessoa):
    def __init__(self, id_pessoa: str, nome: str, email: str, cpf: str, 
                 assinaturas: list = None, perfis: list = None):
        # ... (restante do código do __init__ com atributos privados)
        super().__init__(id_pessoa, nome, email)
        self.__cpf = cpf 
        self.__assinaturas = assinaturas if assinaturas is not None else []
        self.__perfis = perfis if perfis is not None else []
    
    # ... (métodos getters e de negócio)
    
    # ... (restante da classe)

    # --- GETTERS (@property) ---
    @property
    def cpf(self) -> str:
        return self.__cpf

    @property
    def assinaturas(self) -> list:
        return self.__assinaturas
    
    @property
    def perfis(self) -> list:
        return self.__perfis

    # Nota: O método 'papel' foi removido daqui e deve estar em 'Pessoa' ou outra classe base,
    # conforme a orientação do professor.
    
    def adicionar_perfil(self, perfil):
        self.__perfis.append(perfil)

    def adicionar_assinatura(self, assinatura):
        self.__assinaturas.append(assinatura)

    # Nota: Como as Assinaturas e Perfis serão dicionários ao reconstruir a partir do JSON,
    # é necessário um tratamento para garantir que o to_dict funcione corretamente.
    
    def to_dict(self) -> dict:
        base = super().to_dict()
        
        # Serialização defensiva: verifica se o item é um objeto (para chamar to_dict)
        # ou se já é um dicionário (vindo da persistência).
        assinaturas_dict = [a.to_dict() if hasattr(a, 'to_dict') else a for a in self.__assinaturas]
        perfis_dict = [p.to_dict() if hasattr(p, 'to_dict') else p for p in self.__perfis]

        base.update({
            "cpf": self.__cpf,
            "assinaturas": assinaturas_dict,
            "perfis": perfis_dict,
        })
        return base