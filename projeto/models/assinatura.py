# models/assinatura.py
from datetime import date

class Assinatura:
    def __init__(self, id_assinatura: str, id_usuario: str, id_plano: str, status: str = "ativa"):
        self.id_assinatura = id_assinatura
        self.id_usuario = id_usuario
        self.id_plano = id_plano
        self.status = status  # ativa | pausada | cancelada
        self.data_inicio = date.today().isoformat()
        self.data_cancelamento = None
        self.historico = []  # agregação: eventos da assinatura

    def pausar(self):
        if self.status != "ativa":
            raise RuntimeError("Somente assinaturas ativas podem ser pausadas.")
        self.status = "pausada"
        self.historico.append({"evento": "pausa", "data": date.today().isoformat()})

    def retomar(self):
        if self.status != "pausada":
            raise RuntimeError("Somente assinaturas pausadas podem ser retomadas.")
        self.status = "ativa"
        self.historico.append({"evento": "retomada", "data": date.today().isoformat()})

    def cancelar(self):
        if self.status == "cancelada":
            raise RuntimeError("Assinatura já cancelada.")
        self.status = "cancelada"
        self.data_cancelamento = date.today().isoformat()
        self.historico.append({"evento": "cancelamento", "data": self.data_cancelamento})

    def trocar_plano(self, novo_id_plano: str):
        self.historico.append({
            "evento": "troca_plano",
            "de": self.id_plano,
            "para": novo_id_plano,
            "data": date.today().isoformat()
        })
        self.id_plano = novo_id_plano

    def to_dict(self) -> dict:
        return {
            "id_assinatura": self.id_assinatura,
            "id_usuario": self.id_usuario,
            "id_plano": self.id_plano,
            "status": self.status,
            "data_inicio": self.data_inicio,
            "data_cancelamento": self.data_cancelamento,
            "historico": self.historico,
        }
