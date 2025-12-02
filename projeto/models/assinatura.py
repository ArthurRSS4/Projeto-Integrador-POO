# models/assinatura.py
from datetime import date

class Assinatura:
    # Ajuste: Adicionado 'historico' ao __init__ para reconstrução do objeto
    def __init__(self, id_assinatura: str, id_usuario: str, id_plano: str, status: str = "ativa", 
                 data_inicio: str = date.today().isoformat(), data_cancelamento: str = None, 
                 historico: list = None):
        # Atributos PRIVADOS
        self.__id_assinatura = id_assinatura
        self.__id_usuario = id_usuario
        self.__id_plano = id_plano
        self.__status = status  # ativa | pausada | cancelada
        self.__data_inicio = data_inicio
        self.__data_cancelamento = data_cancelamento
        self.__historico = historico if historico is not None else [] 

    # --- GETTERS (@property) ---
    
    @property
    def id_assinatura(self) -> str:
        return self.__id_assinatura

    @property
    def id_usuario(self) -> str:
        return self.__id_usuario
    
    @property
    def id_plano(self) -> str:
        return self.__id_plano

    @property
    def status(self) -> str:
        return self.__status

    @property
    def data_inicio(self) -> str:
        return self.__data_inicio
    
    @property
    def data_cancelamento(self) -> str | None:
        return self.__data_cancelamento
    
    @property
    def historico(self) -> list:
        return self.__historico

    # --- SETTER (Apenas para o que pode ser alterado diretamente) ---
    # Nota: Em POO, o setter para 'status' não é recomendado; é melhor usar o método de negócio (ex: pausar).
    # O 'id_plano' é alterado internamente pelo método 'trocar_plano'.

    # --- MÉTODOS DE NEGÓCIO (Acessando atributos privados) ---
    
    def pausar(self):
        if self.__status != "ativa":
            raise RuntimeError("Somente assinaturas ativas podem ser pausadas.")
        self.__status = "pausada"
        self.__historico.append({"evento": "pausa", "data": date.today().isoformat()})

    def retomar(self):
        if self.__status != "pausada":
            raise RuntimeError("Somente assinaturas pausadas podem ser retomadas.")
        self.__status = "ativa"
        self.__historico.append({"evento": "retomada", "data": date.today().isoformat()})

    def cancelar(self):
        if self.__status == "cancelada":
            raise RuntimeError("Assinatura já cancelada.")
        self.__status = "cancelada"
        self.__data_cancelamento = date.today().isoformat()
        self.__historico.append({"evento": "cancelamento", "data": self.__data_cancelamento})

    def trocar_plano(self, novo_id_plano: str):
        self.__historico.append({
            "evento": "troca_plano",
            "de": self.__id_plano,
            "para": novo_id_plano,
            "data": date.today().isoformat()
        })
        # Atribuição ao atributo privado
        self.__id_plano = novo_id_plano

    def to_dict(self) -> dict:
        return {
            "id_assinatura": self.__id_assinatura,
            "id_usuario": self.__id_usuario,
            "id_plano": self.__id_plano,
            "status": self.__status,
            "data_inicio": self.__data_inicio,
            "data_cancelamento": self.__data_cancelamento,
            "historico": self.__historico,
        }