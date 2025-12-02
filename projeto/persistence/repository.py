# persistence/repository.py
import json
import os
from typing import List, Dict

# Implementa o Padrão de Repositório (DAO) para persistência em JSON
class JSONRepository:
    # Construtor: Inicializa o caminho do arquivo e garante que a pasta 'data/' existe
    def __init__(self, filepath: str):
        self.filepath = filepath
        # Garante que o diretório existe
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        # Se o arquivo não existe, cria-o com uma lista vazia
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    # --- MÉTODOS DE I/O PRIVADOS ---
    
    # Leitura: Lê todo o conteúdo do arquivo JSON
    def _read_all(self) -> List[Dict]:
        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    # Escrita: Sobrescreve todo o arquivo JSON com a nova lista de dados
    def _write_all(self, data: List[Dict]) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    # --- MÉTODOS PÚBLICOS (CRUD) ---

    # Retorna todos os registros
    def list_all(self) -> List[Dict]:
        return self._read_all()

    # Busca um registro pelo valor de uma chave (ex: ID)
    def find_by_id(self, key: str, value: str) -> Dict | None:
        for item in self._read_all():
            if item.get(key) == value:
                return item
        return None

    # Adiciona um novo registro
    def insert(self, obj_dict: Dict) -> None:
        data = self._read_all()
        data.append(obj_dict)
        self._write_all(data)

    # Atualiza um registro existente
    def update(self, key: str, value: str, new_dict: Dict) -> bool:
        data = self._read_all()
        updated = False # Flag para rastrear a alteração
        
        # Itera para encontrar e atualizar o registro
        for i, item in enumerate(data):
            if item.get(key) == value:
                data[i] = new_dict
                updated = True
                # OTIMIZAÇÃO: Interrompe o loop imediatamente (performance)
                break 
        
        # OTIMIZAÇÃO: Escreve no arquivo APENAS se houve alteração
        if updated:
            self._write_all(data)
            return True
            
        return False

    # Exclui um registro
    def delete(self, key: str, value: str) -> bool:
        data = self._read_all()
        # Cria uma nova lista sem o registro a ser removido
        new_data = [d for d in data if d.get(key) != value]
        removed = len(new_data) != len(data)
        if removed:
            self._write_all(new_data)
        return removed