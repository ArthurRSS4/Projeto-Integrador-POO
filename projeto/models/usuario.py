# models/usuario.py
from .pessoa import Pessoa # Importa a classe base Pessoa (Herança)
from datetime import date 

class Usuario(Pessoa):
    # Construtor: Inicializa o usuário, chamando o construtor da classe base (Pessoa)
    def __init__(self, id_pessoa: str, nome: str, email: str, cpf: str, 
                 assinaturas: list = None, perfis: list = None):
        
        # Chama o construtor da classe Pessoa (Herança)
        super().__init__(id_pessoa, nome, email)
        
        # Atributos PRIVADOS
        self.__cpf = cpf 
        self.__assinaturas = assinaturas if assinaturas is not None else [] # Composição: Usuário possui Assinaturas
        self.__perfis = perfis if perfis is not None else [] # Composição: Usuário possui Perfis
    
    # --- GETTERS (@property) ---
    # Permitem a leitura controlada dos atributos privados
    @property
    def cpf(self) -> str:
        return self.__cpf

    @property
    def assinaturas(self) -> list:
        return self.__assinaturas
    
    @property
    def perfis(self) -> list:
        return self.__perfis
    
    # --- MÉTODOS DE NEGÓCIO ---
    
    # Adiciona um Perfil à lista (Composição)
    def adicionar_perfil(self, perfil):
        self.__perfis.append(perfil)

    # Adiciona uma Assinatura à lista (Composição)
    def adicionar_assinatura(self, assinatura):
        self.__assinaturas.append(assinatura)

    # Método de Serialização: Converte o objeto para dicionário (usado pelo JSONRepository)
    def to_dict(self) -> dict:
        # Pega os dados básicos da classe Pessoa
        base = super().to_dict()
        
        # Serializa listas de objetos filhos (Assinaturas e Perfis) para dicionários
        assinaturas_dict = [a.to_dict() if hasattr(a, 'to_dict') else a for a in self.__assinaturas]
        perfis_dict = [p.to_dict() if hasattr(p, 'to_dict') else p for p in self.__perfis]

        # Adiciona atributos específicos do Usuário
        base.update({
            "cpf": self.__cpf,
            "assinaturas": assinaturas_dict,
            "perfis": perfis_dict,
        })
        return base