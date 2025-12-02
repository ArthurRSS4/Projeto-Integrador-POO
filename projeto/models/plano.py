# models/plano.py
# Lembrete: Adicionar a importação: from ..utils.validator import Validator

class Plano:
    # Construtor: Inicializa as características do plano.
    def __init__(self, id_plano: str, nome: str, preco_mensal: float, num_telas: int, qualidade: str):
        # Uso do Validator: Garante que o preço inicial é positivo
        Validator.preco(preco_mensal)
        
        # Atributos PRIVADOS (Encapsulamento)
        self.__id_plano = id_plano
        self.__nome = nome
        self.__preco_mensal = preco_mensal
        self.__num_telas = num_telas
        self.__qualidade = qualidade
        
    # --- GETTERS (@property) ---
    # Permitem a leitura controlada dos atributos privados
    @property
    def id_plano(self) -> str:
        return self.__id_plano
        
    @property
    def preco_mensal(self) -> float:
        return self.__preco_mensal
        
    @property
    def nome(self) -> str:
        return self.__nome

    @property
    def num_telas(self) -> int:
        return self.__num_telas

    @property
    def qualidade(self) -> str:
        return self.__qualidade
    
    # --- MÉTODO DE NEGÓCIO (Ajuste de Preço) ---
    def ajustar_preco(self, novo_preco: float):
        """Ajusta o preço mensal do plano após validação."""
        # Regra: Revalida o novo preço antes de aplicá-lo
        Validator.preco(novo_preco)
        self.__preco_mensal = novo_preco

    # Método de Serialização: Converte o objeto para dicionário (usado pelo JSONRepository)
    def to_dict(self) -> dict:
        return {
            "id_plano": self.__id_plano,
            "nome": self.__nome,
            "preco_mensal": self.__preco_mensal,
            "num_telas": self.__num_telas,
            "qualidade": self.__qualidade,
        }