# models/plano.py
class Plano:
    def __init__(self, id_plano: str, nome: str, preco_mensal: float, qtd_telas: int, qualidade: str):
        self.id_plano = id_plano
        self.nome = nome
        self.preco_mensal = preco_mensal
        self.qtd_telas = qtd_telas
        self.qualidade = qualidade  # SD/HD/4K

    def aplicar_desconto(self, percentual: float) -> float:
        if percentual < 0 or percentual > 50:
            raise ValueError("Percentual de desconto inválido (0–50).")
        return round(self.preco_mensal * (1 - percentual / 100), 2)

    def to_dict(self) -> dict:
        return {
            "id_plano": self.id_plano,
            "nome": self.nome,
            "preco_mensal": self.preco_mensal,
            "qtd_telas": self.qtd_telas,
            "qualidade": self.qualidade,
        }
