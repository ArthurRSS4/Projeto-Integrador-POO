# main.py
from models.usuario import Usuario
from models.plano import Plano
from models.assinatura import Assinatura
from models.perfil import Perfil
from models.pagamento import Pagamento
from persistence.repository import JSONRepository
from utils.validator import Validator
from utils.logger import Logger

# --- NOVAS IMPORTAÇÕES DO RICH ---
from rich.console import Console
from rich.table import Table
import uuid

# --- INICIALIZAÇÃO DO CONSOLE RICH ---
logger = Logger()
console = Console() # Objeto Rich para todas as saídas

repo_usuarios = JSONRepository("data/usuarios.json")
repo_planos = JSONRepository("data/planos.json")
repo_assinaturas = JSONRepository("data/assinaturas.json")
repo_pagamentos = JSONRepository("data/pagamentos.json")

def gerar_id(prefixo: str) -> str:
    return f"{prefixo}_{uuid.uuid4().hex[:8]}"

def seed_planos():
    if not repo_planos.list_all():
        # Certifique-se de que os dados aqui também estão serializando atributos privados
        planos = [
            Plano("pln_basic", "Basic", 19.90, 1, "SD").to_dict(),
            Plano("pln_standard", "Standard", 34.90, 2, "HD").to_dict(),
            Plano("pln_premium", "Premium", 54.90, 4, "4K").to_dict(),
        ]
        for p in planos:
            repo_planos.insert(p)
        logger.info("Planos iniciais criados.")

def cadastrar_usuario():
    nome = console.input("[yellow]Nome:[/yellow] ").strip()
    email = console.input("[yellow]Email:[/yellow] ").strip()
    cpf = console.input("[yellow]CPF (11 dígitos):[/yellow] ").strip()

    if not Validator.email(email):
        console.print("[bold red]Email inválido.[/bold red]")
        return
    if not Validator.cpf(cpf):
        console.print("[bold red]CPF inválido.[/bold red]")
        return

    usuario = Usuario(gerar_id("usr"), nome, email, cpf)
    repo_usuarios.insert(usuario.to_dict())
    logger.info(f"Usuário cadastrado: {usuario.id_pessoa}")
    console.print("[bold green]Usuário cadastrado com sucesso.[/bold green]")

def listar_usuarios():
    table = Table(title="Lista de Usuários", show_header=True, header_style="bold cyan")
    table.add_column("ID", style="dim", width=12)
    table.add_column("Nome")
    table.add_column("Email", style="yellow")
    
    for u in repo_usuarios.list_all():
        table.add_row(u['id_pessoa'], u['nome'], u['email'])
        
    console.print(table)

def excluir_usuario():
    idu = console.input("[yellow]ID do usuário:[/yellow] ").strip()
    ok = repo_usuarios.delete("id_pessoa", idu)
    if ok:
        console.print("[bold green]Excluído.[/bold green]")
    else:
        console.print("[bold red]Não encontrado.[/bold red]")

def criar_assinatura():
    idu = console.input("[yellow]ID do usuário:[/yellow] ").strip()
    usuario = repo_usuarios.find_by_id("id_pessoa", idu)
    if not usuario:
        console.print("[bold red]Usuário não encontrado.[/bold red]")
        return

    # LISTAGEM DE PLANOS COM RICH TABLE
    table = Table(title="Planos Disponíveis", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=12)
    table.add_column("Nome")
    table.add_column("Preço Mensal (R$)", justify="right", style="green")
    
    planos = repo_planos.list_all()
    for p in planos:
        table.add_row(p['id_plano'], p['nome'], f"{p['preco_mensal']:.2f}")

    console.print(table)

    idp = console.input("[yellow]ID do plano:[/yellow] ").strip()
    plano = next((p for p in planos if p["id_plano"] == idp), None)
    if not plano:
        console.print("[bold red]Plano não encontrado.[/bold red]")
        return

    assinatura = Assinatura(gerar_id("asn"), idu, idp)
    repo_assinaturas.insert(assinatura.to_dict())
    logger.info(f"Assinatura criada: {assinatura.id_assinatura}")
    console.print("[bold green]Assinatura criada com sucesso.[/bold green]")

# ... (Outras funções de negócio: trocar_plano, cancelar_assinatura, registrar_pagamento) ...

def listar_assinaturas():
    table = Table(title="Lista de Assinaturas", show_header=True, header_style="bold yellow")
    table.add_column("ID", style="dim", width=12)
    table.add_column("Usuário ID")
    table.add_column("Plano ID")
    table.add_column("Status", style="bold")
    
    for a in repo_assinaturas.list_all():
        status_color = "green" if a['status'] == "ativa" else "red" if a['status'] == "cancelada" else "yellow"
        table.add_row(a['id_assinatura'], a['id_usuario'], a['id_plano'], f"[{status_color}]{a['status']}[/{status_color}]")
        
    console.print(table)

def menu():
    seed_planos()
    while True:
        console.print("\n[bold blue]Menu Principal[/bold blue]")
        console.print("1 - Cadastrar usuário")
        console.print("2 - Excluir usuário")
        console.print("3 - Listar usuários")
        console.print("4 - Criar assinatura")
        console.print("5 - Trocar plano da assinatura")
        console.print("6 - Cancelar assinatura")
        console.print("7 - Registrar pagamento")
        console.print("8 - Listar assinaturas")
        console.print("0 - [bold red]Sair[/bold red]")
        op = console.input("[bold]>[/bold] ").strip()
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
            else: console.print("[bold red]Opção inválida.[/bold red]")
        except Exception as e:
            logger.error(str(e))
            console.print(f"[bold red]ERRO:[/bold red] {e}")

if __name__ == "__main__":
    menu()