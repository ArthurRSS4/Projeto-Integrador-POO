# persistence/repository.py
import json
import os
from typing import List, Dict

class JSONRepository:
    def __init__(self, filepath: str):
        self.filepath = filepath
        os.makedirs(os.path.dirname(filepath), exist_ok=True)
        if not os.path.exists(filepath):
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump([], f, ensure_ascii=False, indent=2)

    def _read_all(self) -> List[Dict]:
        with open(self.filepath, "r", encoding="utf-8") as f:
            return json.load(f)

    def _write_all(self, data: List[Dict]) -> None:
        with open(self.filepath, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def list_all(self) -> List[Dict]:
        return self._read_all()

    def find_by_id(self, key: str, value: str) -> Dict | None:
        for item in self._read_all():
            if item.get(key) == value:
                return item
        return None

    def insert(self, obj_dict: Dict) -> None:
        data = self._read_all()
        data.append(obj_dict)
        self._write_all(data)

    def update(self, key: str, value: str, new_dict: Dict) -> bool:
        data = self._read_all()
        updated = False # Flag para rastrear se o item foi encontrado e alterado
        
        for i, item in enumerate(data):
            if item.get(key) == value:
                data[i] = new_dict
                updated = True
                # CORREÇÃO: Usamos 'break' para sair do loop imediatamente após encontrar o item.
                break 
        
        # CORREÇÃO: Escrever no arquivo APENAS UMA VEZ, se houver alteração.
        if updated:
            self._write_all(data)
            return True
            
        return False

    def delete(self, key: str, value: str) -> bool:
        data = self._read_all()
        new_data = [d for d in data if d.get(key) != value]
        removed = len(new_data) != len(data)
        if removed:
            self._write_all(new_data)
        return removed
