# models/plano.py (Bloco sugerido)

class Plano:
    def __init__(self, id_plano: str, nome: str, preco_mensal: float, num_telas: int, qualidade: str):
        # Uso do Validator na criação
        Validator.preco(preco_mensal)
        
        self.__id_plano = id_plano
        self.__nome = nome
        self.__preco_mensal = preco_mensal
        self.__num_telas = num_telas
        self.__qualidade = qualidade
        
    # --- GETTERS (@property) ---
    @property
    def id_plano(self) -> str:
        return self.__id_plano
        
    @property
    def preco_mensal(self) -> float:
        return self.__preco_mensal
        
    # ... outros getters (nome, num_telas, qualidade)
    
    # --- MÉTODO DE NEGÓCIO (Adicional, para atender à regra geral) ---
    def ajustar_preco(self, novo_preco: float):
        """Ajusta o preço mensal do plano após validação."""
        Validator.preco(novo_preco)
        self.__preco_mensal = novo_preco

    def to_dict(self) -> dict:
        return {
            "id_plano": self.__id_plano,
            "nome": self.__nome,
            "preco_mensal": self.__preco_mensal,
            "num_telas": self.__num_telas,
            "qualidade": self.__qualidade,
        }