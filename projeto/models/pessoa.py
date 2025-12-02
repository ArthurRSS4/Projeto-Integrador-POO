# models/pessoa.py (Bloco sugerido)

class Pessoa:
    def __init__(self, id_pessoa: str, nome: str, email: str):
        self.__id_pessoa = id_pessoa
        self.__nome = nome
        self.__email = email
    
    # --- GETTERS (@property) ---
    @property
    def id_pessoa(self) -> str:
        return self.__id_pessoa
    
    @property
    def nome(self) -> str:
        return self.__nome
    
    @property
    def email(self) -> str:
        return self.__email
        
    # --- MÉTODO DE POLIMORFISMO (Obrigatório para subclasses) ---
    def papel(self) -> str:
        """
        Retorna o papel específico da pessoa no sistema.
        Deve ser sobrescrito pelas subclasses (ex: Usuario, Admin).
        """
        # Levantar um erro ou retornar um valor neutro aqui é uma boa prática
        return "Pessoa Base" 
        
    def to_dict(self) -> dict:
        return {
            "id_pessoa": self.__id_pessoa,
            "nome": self.__nome,
            "email": self.__email,
        }