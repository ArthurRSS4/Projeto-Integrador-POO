# models/pagamento.py
from datetime import date
from utils.validator import Validator # Importar o Validator para checagem de preço

class Pagamento:
    def __init__(self, id_pagamento: str, id_assinatura: str, valor: float, metodo: str, status: str = "pendente", 
                 data_pagamento: str = date.today().isoformat(), data_confirmacao: str = None):
        
        # O Validator pode ser usado aqui para garantir a integridade dos dados na criação
        Validator.preco(valor)
        
        # Atributos PRIVADOS
        self.__id_pagamento = id_pagamento
        self.__id_assinatura = id_assinatura
        self.__valor = valor
        self.__metodo = metodo
        self.__status = status # pendente | confirmado | falhado | estornado
        self.__data_pagamento = data_pagamento
        self.__data_confirmacao = data_confirmacao

    # --- GETTERS (@property) ---
    @property
    def id_pagamento(self) -> str:
        return self.__id_pagamento
    
    @property
    def valor(self) -> float:
        return self.__valor

    @property
    def status(self) -> str:
        return self.__status

    # ... Adicionar outros getters (id_assinatura, metodo, data_pagamento, data_confirmacao)
    
    # --- MÉTODO DE NEGÓCIO 1: Confirmação ---
    def confirmar_pagamento(self):
        """Marca o pagamento como confirmado, registrando a data."""
        if self.__status != "pendente":
            raise RuntimeError(f"O pagamento já está com status: {self.__status}. Não pode ser confirmado.")
        
        self.__status = "confirmado"
        self.__data_confirmacao = date.today().isoformat()

    # --- MÉTODO DE NEGÓCIO 2: Estorno/Reembolso ---
    def estornar(self):
        """Reverte o pagamento, mudando o status para 'estornado'."""
        if self.__status != "confirmado":
            raise RuntimeError(f"Somente pagamentos confirmados podem ser estornados. Status atual: {self.__status}.")
        
        # Aqui, poderíamos adicionar lógica de comunicação com um gateway de pagamento real, se existisse.
        self.__status = "estornado"
        self.__data_confirmacao = None # Opcional: Remover data de confirmação ou adicionar data de estorno
        
    def to_dict(self) -> dict:
        return {
            "id_pagamento": self.__id_pagamento,
            "id_assinatura": self.__id_assinatura,
            "valor": self.__valor,
            "metodo": self.__metodo,
            "status": self.__status,
            "data_pagamento": self.__data_pagamento,
            "data_confirmacao": self.__data_confirmacao,
        }