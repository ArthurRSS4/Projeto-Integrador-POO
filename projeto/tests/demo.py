# projeto/tests/demo.py
import json
# Importa as classes de Modelo para instanciar objetos
from projeto.models.usuario import Usuario
from projeto.models.plano import Plano
from projeto.models.assinatura import Assinatura

# Função principal de demonstração
def run_demo():
    # Instanciação de Objetos (Composição / Associação)
    u = Usuario("usr_demo", "Arthur", "arthur@example.com", "12345678901")
    p = Plano("pln_demo", "Demo", 29.99, 1, "SD")
    a = Assinatura("asn_demo", u.id_pessoa, p.id_plano)

    # --- Teste dos Métodos de Negócio (Regras e Encapsulamento) ---
    
    # Demonstra o método de negócio (regra: só pausa se estiver ativa)
    a.pausar()
    # Demonstra o método de negócio (regra: só retoma se estiver pausada)
    a.retomar()
    # Demonstra a troca de plano e registro no histórico
    a.trocar_plano("pln_demo2")
    # Demonstra o método de negócio final (regra: muda status para 'cancelada')
    a.cancelar()

    # --- Saída dos Dados ---
    
    print("\n--- Usuário ---")
    print(f"ID: {u.id_pessoa} | Nome: {u.nome} | Email: {u.email} | CPF: {u.cpf}")

    print("\n--- Plano ---")
    # Chama o to_dict() para serializar o objeto
    print(json.dumps(p.to_dict(), indent=2, ensure_ascii=False))

    print("\n--- Assinatura (Exemplo de Serialização e Histórico) ---")
    # Mostra o histórico de eventos da assinatura
    print(json.dumps(a.to_dict(), indent=2, ensure_ascii=False))

# Ponto de entrada do script
if __name__ == "__main__":
    run_demo()