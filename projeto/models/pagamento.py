# models/pagamento.py
from datetime import date
from utils.validator import Validator # Importa o Validador para garantir integridade

class Pagamento:
    # Construtor: Inicializa o pagamento com status 'pendente' por padrão
    def __init__(self, id_pagamento: str, id_assinatura: str, valor: float, metodo: str, status: str = "pendente", 
                 data_pagamento: str = date.today().isoformat(), data_confirmacao: str = None):
        
        # Uso do Validator: Garante que o valor é positivo
        Validator.preco(valor)
        
        # Atributos PRIVADOS (Encapsulamento)
        self.__id_pagamento = id_pagamento
        self.__id_assinatura = id_assinatura
        self.__valor = valor
        self.__metodo = metodo
        self.__status = status # status: pendente | confirmado | falhado | estornado
        self.__data_pagamento = data_pagamento
        self.__data_confirmacao = data_confirmacao

    # --- GETTERS (@property) ---
    # Permitem a leitura controlada dos atributos privados
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
    # Regra: Altera o estado de 'pendente' para 'confirmado'
    def confirmar_pagamento(self):
        """Marca o pagamento como confirmado, registrando a data."""
        if self.__status != "pendente":
            raise RuntimeError(f"O pagamento já está com status: {self.__status}. Não pode ser confirmado.")
        
        self.__status = "confirmado"
        self.__data_confirmacao = date.today().isoformat()

    # --- MÉTODO DE NEGÓCIO 2: Estorno/Reembolso ---
    # Regra: Altera o estado de 'confirmado' para 'estornado'
    def estornar(self):
        """Reverte o pagamento, mudando o status para 'estornado'."""
        if self.__status != "confirmado":
            raise RuntimeError(f"Somente pagamentos confirmados podem ser estornados. Status atual: {self.__status}.")
        
        # Lógica de estorno
        self.__status = "estornado"
        self.__data_confirmacao = None 
        
    # Método de Serialização: Converte o objeto para dicionário (usado pelo JSONRepository)
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