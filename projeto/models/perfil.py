# models/perfil.py (Bloco sugerido)

class Perfil:
    def __init__(self, id_perfil: str, nome: str, idade: int, genero: str):
        self.__id_perfil = id_perfil
        self.__nome = nome
        self.__idade = idade
        self.__genero = genero # NOVO ATRIBUTO
        
    # --- GETTERS (@property) ---
    # ... (id_perfil, nome, idade)
    
    @property
    def genero(self) -> str:
        return self.__genero
    
    # --- SETTER (Exemplo) ---
    @genero.setter
    def genero(self, novo_genero: str):
        # Aqui, você pode adicionar validação para garantir que o gênero seja válido
        self.__genero = novo_genero

    def to_dict(self) -> dict:
        return {
            "id_perfil": self.__id_perfil,
            "nome": self.__nome,
            "idade": self.__idade,
            "genero": self.__genero,
        }