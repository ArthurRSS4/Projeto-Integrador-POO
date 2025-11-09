# models/pagamento.py
from datetime import date

class Pagamento:
    def __init__(self, id_pagamento: str, id_assinatura: str, valor: float, metodo: str):
        self.id_pagamento = id_pagamento
        self.id_assinatura = id_assinatura
        self.valor = round(valor, 2)
        self.metodo = metodo  # cartão, pix, boleto
        self.data = date.today().isoformat()
        self.status = "liquidado"  # liquidado | pendente | falhado

    def marcar_falha(self, motivo: str):
        self.status = "falhado"
        self.motivo = motivo

    def to_dict(self) -> dict:
        return {
            "id_pagamento": self.id_pagamento,
            "id_assinatura": self.id_assinatura,
            "valor": self.valor,
            "metodo": self.metodo,
            "data": self.data,
            "status": self.status,
        }
