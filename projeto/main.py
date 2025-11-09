# main.py
from models.usuario import Usuario
from models.plano import Plano
from models.assinatura import Assinatura
from models.perfil import Perfil
from models.pagamento import Pagamento
from persistence.repository import JSONRepository
from utils.validator import Validator
from utils.logger import Logger

import uuid

logger = Logger()

repo_usuarios = JSONRepository("data/usuarios.json")
repo_planos = JSONRepository("data/planos.json")
repo_assinaturas = JSONRepository("data/assinaturas.json")
repo_pagamentos = JSONRepository("data/pagamentos.json")

def gerar_id(prefixo: str) -> str:
    return f"{prefixo}_{uuid.uuid4().hex[:8]}"

def seed_planos():
    if not repo_planos.list_all():
        planos = [
            Plano("pln_basic", "Basic", 19.90, 1, "SD").to_dict(),
            Plano("pln_standard", "Standard", 34.90, 2, "HD").to_dict(),
            Plano("pln_premium", "Premium", 54.90, 4, "4K").to_dict(),
        ]
        for p in planos:
            repo_planos.insert(p)
        logger.info("Planos iniciais criados.")

def cadastrar_usuario():
    nome = input("Nome: ").strip()
    email = input("Email: ").strip()
    cpf = input("CPF (11 dígitos): ").strip()

    if not Validator.email(email):
        print("Email inválido.")
        return
    if not Validator.cpf(cpf):
        print("CPF inválido.")
        return

    usuario = Usuario(gerar_id("usr"), nome, email, cpf)
    repo_usuarios.insert(usuario.to_dict())
    logger.info(f"Usuário cadastrado: {usuario.id_pessoa}")
    print("Usuário cadastrado com sucesso.")

def listar_usuarios():
    for u in repo_usuarios.list_all():
        print(f"- {u['id_pessoa']} | {u['nome']} | {u['email']}")

def excluir_usuario():
    idu = input("ID do usuário: ").strip()
    ok = repo_usuarios.delete("id_pessoa", idu)
    print("Excluído." if ok else "Não encontrado.")

def criar_assinatura():
    idu = input("ID do usuário: ").strip()
    usuario = repo_usuarios.find_by_id("id_pessoa", idu)
    if not usuario:
        print("Usuário não encontrado.")
        return

    print("Planos disponíveis:")
    planos = repo_planos.list_all()
    for p in planos:
        print(f"- {p['id_plano']} | {p['nome']} | R$ {p['preco_mensal']}")

    idp = input("ID do plano: ").strip()
    plano = next((p for p in planos if p["id_plano"] == idp), None)
    if not plano:
        print("Plano não encontrado.")
        return

    assinatura = Assinatura(gerar_id("asn"), idu, idp)
    repo_assinaturas.insert(assinatura.to_dict())
    logger.info(f"Assinatura criada: {assinatura.id_assinatura}")
    print("Assinatura criada com sucesso.")

def trocar_plano():
    ida = input("ID da assinatura: ").strip()
    assinatura = repo_assinaturas.find_by_id("id_assinatura", ida)
    if not assinatura:
        print("Assinatura não encontrada.")
        return
    idp = input("Novo ID de plano: ").strip()
    plano = repo_planos.find_by_id("id_plano", idp)
    if not plano:
        print("Plano não encontrado.")
        return

    from models.assinatura import Assinatura as AssinaturaModel
    obj = AssinaturaModel(**{
        "id_assinatura": assinatura["id_assinatura"],
        "id_usuario": assinatura["id_usuario"],
        "id_plano": assinatura["id_plano"],
        "status": assinatura["status"]
    })
    obj.historico = assinatura.get("historico", [])
    obj.data_inicio = assinatura.get("data_inicio")
    obj.data_cancelamento = assinatura.get("data_cancelamento")

    obj.trocar_plano(idp)
    repo_assinaturas.update("id_assinatura", ida, obj.to_dict())
    logger.info(f"Assinatura {ida} trocou para plano {idp}")
    print("Plano trocado com sucesso.")

def cancelar_assinatura():
    ida = input("ID da assinatura: ").strip()
    assinatura = repo_assinaturas.find_by_id("id_assinatura", ida)
    if not assinatura:
        print("Assinatura não encontrada.")
        return

    from models.assinatura import Assinatura as AssinaturaModel
    obj = AssinaturaModel(**{
        "id_assinatura": assinatura["id_assinatura"],
        "id_usuario": assinatura["id_usuario"],
        "id_plano": assinatura["id_plano"],
        "status": assinatura["status"]
    })
    obj.historico = assinatura.get("historico", [])
    obj.cancelar()
    repo_assinaturas.update("id_assinatura", ida, obj.to_dict())
    logger.info(f"Assinatura {ida} cancelada")
    print("Assinatura cancelada.")

def registrar_pagamento():
    ida = input("ID da assinatura: ").strip()
    assinatura = repo_assinaturas.find_by_id("id_assinatura", ida)
    if not assinatura:
        print("Assinatura não encontrada.")
        return
    plano = repo_planos.find_by_id("id_plano", assinatura["id_plano"])
    valor = float(plano["preco_mensal"])
    metodo = input("Método (cartao/pix/boleto): ").strip()
    pagamento = Pagamento(gerar_id("pay"), ida, valor, metodo)
    repo_pagamentos.insert(pagamento.to_dict())
    logger.info(f"Pagamento {pagamento.id_pagamento} registrado")
    print("Pagamento registrado.")

def listar_assinaturas():
    for a in repo_assinaturas.list_all():
        print(f"- {a['id_assinatura']} | usuario={a['id_usuario']} | plano={a['id_plano']} | status={a['status']}")

def menu():
    seed_planos()
    while True:
        print("\nMenu principal")
        print("1 - Cadastrar usuário")
        print("2 - Excluir usuário")
        print("3 - Listar usuários")
        print("4 - Criar assinatura")
        print("5 - Trocar plano da assinatura")
        print("6 - Cancelar assinatura")
        print("7 - Registrar pagamento")
        print("8 - Listar assinaturas")
        print("0 - Sair")
        op = input("> ").strip()
        try:
            if op == "1": cadastrar_usuario()
            elif op == "2": excluir_usuario()
            elif op == "3": listar_usuarios()
            elif op == "4": criar_assinatura()
            elif op == "5": trocar_plano()
            elif op == "6": cancelar_assinatura()
            elif op == "7": registrar_pagamento()
            elif op == "8": listar_assinaturas()
            elif op == "0": break
            else: print("Opção inválida.")
        except Exception as e:
            logger.error(str(e))
            print(f"Erro: {e}")

if __name__ == "__main__":
    menu()
