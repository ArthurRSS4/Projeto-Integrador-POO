# models/pessoa.py

class Pessoa:
    # Construtor: Classe base que define atributos comuns a todos os tipos de pessoas
    def __init__(self, id_pessoa: str, nome: str, email: str):
        # Atributos PRIVADOS (Encapsulamento)
        self.__id_pessoa = id_pessoa
        self.__nome = nome
        self.__email = email
    
    # --- GETTERS (@property) ---
    # Permitem a leitura controlada dos atributos privados
    @property
    def id_pessoa(self) -> str:
        return self.__id_pessoa
    
    @property
    def nome(self) -> str:
        return self.__nome
    
    @property
    def email(self) -> str:
        return self.__email
        
    # --- MÉTODO DE POLIMORFISMO (Método de Negócio) ---
    def papel(self) -> str:
        """
        Define o papel da pessoa no sistema.
        É o método que será SOBRESCRITO por classes filhas (ex: Usuario) para aplicar o Polimorfismo.
        """
        return "Pessoa Base" 
        
    # Método de Serialização: Converte o objeto para dicionário (usado pelo JSONRepository)
    def to_dict(self) -> dict:
        return {
            "id_pessoa": self.__id_pessoa,
            "nome": self.__nome,
            "email": self.__email,
        }