# projeto/tests/demo.py
import json
from projeto.models.usuario import Usuario
from projeto.models.plano import Plano
from projeto.models.assinatura import Assinatura

def run_demo():
    # Criando objetos de exemplo
    u = Usuario("usr_demo", "Arthur", "arthur@example.com", "12345678901")
    p = Plano("pln_demo", "Demo", 29.99, 1, "SD")
    a = Assinatura("asn_demo", u.id_pessoa, p.id_plano)

    # Operações de negócio
    a.pausar()
    a.retomar()
    a.trocar_plano("pln_demo2")
    a.cancelar()

    print("\n--- Usuário ---")
    print(f"ID: {u.id_pessoa} | Nome: {u.nome} | Email: {u.email} | CPF: {u.cpf}")

    print("\n--- Plano ---")
    print(json.dumps(p.to_dict(), indent=2, ensure_ascii=False))

    print("\n--- Assinatura ---")
    print(json.dumps(a.to_dict(), indent=2, ensure_ascii=False))

if __name__ == "__main__":
    run_demo()
