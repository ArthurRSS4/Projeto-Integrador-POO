# models/perfil.py
class Perfil:
    def __init__(self, id_perfil: str, nome: str, controle_parental: bool = False):
        self.id_perfil = id_perfil
        self.nome = nome
        self.controle_parental = controle_parental
        self.preferencias = {"idioma": "pt-BR", "generos": []}

    def adicionar_genero(self, genero: str):
        if genero not in self.preferencias["generos"]:
            self.preferencias["generos"].append(genero)

    def to_dict(self) -> dict:
        return {
            "id_perfil": self.id_perfil,
            "nome": self.nome,
            "controle_parental": self.controle_parental,
            "preferencias": self.preferencias,
        }
