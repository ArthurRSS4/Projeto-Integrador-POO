# models/perfil.py

class Perfil:
    # Construtor: Inicializa um novo perfil.
    def __init__(self, id_perfil: str, nome: str, idade: int, genero: str):
        # Atributos PRIVADOS (Encapsulamento)
        self.__id_perfil = id_perfil
        self.__nome = nome
        self.__idade = idade
        self.__genero = genero # NOVO ATRIBUTO solicitado pelo professor
        
    # --- GETTERS (@property) ---
    # Permitem a leitura controlada dos atributos privados
    
    @property
    def id_perfil(self) -> str:
        return self.__id_perfil
        
    @property
    def nome(self) -> str:
        return self.__nome
        
    @property
    def idade(self) -> int:
        return self.__idade
    
    @property
    def genero(self) -> str:
        return self.__genero
    
    # --- SETTER (Para o atributo 'genero') ---
    # Permite alterar o valor do atributo privado (setter)
    @genero.setter
    def genero(self, novo_genero: str):
        # Aqui, poderíamos adicionar a lógica de validação
        self.__genero = novo_genero

    # Método de Serialização: Converte o objeto para dicionário (usado pelo JSONRepository)
    def to_dict(self) -> dict:
        return {
            "id_perfil": self.__id_perfil,
            "nome": self.__nome,
            "idade": self.__idade,
            "genero": self.__genero,
        }