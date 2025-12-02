# main.py
# --- IMPORTAÇÕES DA CAMADA DE MODELOS (Lógica de Negócio) ---
from models.usuario import Usuario
from models.plano import Plano
from models.assinatura import Assinatura
from models.perfil import Perfil
from models.pagamento import Pagamento
# --- IMPORTAÇÕES DA CAMADA DE PERSISTÊNCIA E UTILIDADES ---
from persistence.repository import JSONRepository
from utils.validator import Validator
from utils.logger import Logger

# --- IMPORTAÇÕES DO RICH (Interface do Usuário) ---
from rich.console import Console
from rich.table import Table
import uuid

# --- INICIALIZAÇÃO E INJEÇÃO DE DEPENDÊNCIAS ---
logger = Logger()
console = Console() # Objeto Rich: Melhora a apresentação CLI

# Instanciação dos Repositórios (Persistência)
repo_usuarios = JSONRepository("data/usuarios.json")
repo_planos = JSONRepository("data/planos.json")
repo_assinaturas = JSONRepository("data/assinaturas.json")
repo_pagamentos = JSONRepository("data/pagamentos.json")

# Função auxiliar para gerar IDs únicos
def gerar_id(prefixo: str) -> str:
    return f"{prefixo}_{uuid.uuid4().hex[:8]}"

# Cria planos iniciais se o arquivo estiver vazio (Seed inicial)
def seed_planos():
    if not repo_planos.list_all():
        # Cria objetos Plano e os insere no repositório
        planos = [
            Plano("pln_basic", "Basic", 19.90, 1, "SD").to_dict(),
            Plano("pln_standard", "Standard", 34.90, 2, "HD").to_dict(),
            Plano("pln_premium", "Premium", 54.90, 4, "4K").to_dict(),
        ]
        for p in planos:
            repo_planos.insert(p)
        logger.info("Planos iniciais criados.")

# --- FUNÇÕES DE NEGÓCIO (CRUD) ---

def cadastrar_usuario():
    nome = console.input("[yellow]Nome:[/yellow] ").strip()
    email = console.input("[yellow]Email:[/yellow] ").strip()
    cpf = console.input("[yellow]CPF (11 dígitos):[/yellow] ").strip()

    # Usa o Validator para verificar a entrada
    if not Validator.email(email) or not Validator.cpf(cpf):
        console.print("[bold red]Dados inválidos.[/bold red]")
        return

    # Cria o objeto, o serializa e salva usando o Repositório
    usuario = Usuario(gerar_id("usr"), nome, email, cpf)
    repo_usuarios.insert(usuario.to_dict())
    logger.info(f"Usuário cadastrado: {usuario.id_pessoa}")
    console.print("[bold green]Usuário cadastrado com sucesso.[/bold green]")

def listar_usuarios():
    # Cria uma Tabela Rich para formatação visual
    table = Table(title="Lista de Usuários", show_header=True, header_style="bold cyan")
    table.add_column("ID", style="dim", width=12)
    table.add_column("Nome")
    table.add_column("Email", style="yellow")
    
    # Carrega dados do Repositório e popula a tabela
    for u in repo_usuarios.list_all():
        table.add_row(u['id_pessoa'], u['nome'], u['email'])
        
    console.print(table)

def excluir_usuario():
    idu = console.input("[yellow]ID do usuário:[/yellow] ").strip()
    # Chama o método delete do Repositório
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

    # Cria o objeto Assinatura e salva no Repositório
    assinatura = Assinatura(gerar_id("asn"), idu, idp)
    repo_assinaturas.insert(assinatura.to_dict())
    logger.info(f"Assinatura criada: {assinatura.id_assinatura}")
    console.print("[bold green]Assinatura criada com sucesso.[/bold green]")


def trocar_plano():
    ida = console.input("[yellow]ID da assinatura:[/yellow] ").strip()
    assinatura_data = repo_assinaturas.find_by_id("id_assinatura", ida)
    if not assinatura_data:
        console.print("[bold red]Assinatura não encontrada.[/bold red]")
        return

    # 1. Carregar o objeto para aplicar a regra de negócio
    a = Assinatura(**assinatura_data)

    # Exibe planos disponíveis
    planos = repo_planos.list_all()
    table = Table(title="Planos Disponíveis", show_header=True, header_style="bold magenta")
    table.add_column("ID", style="dim", width=12)
    table.add_column("Nome")
    table.add_column("Preço Mensal (R$)", justify="right", style="green")
    for p in planos:
        table.add_row(p['id_plano'], p['nome'], f"{p['preco_mensal']:.2f}")
    console.print(table)

    novo_idp = console.input("[yellow]Novo ID do plano:[/yellow] ").strip()
    plano = next((p for p in planos if p["id_plano"] == novo_idp), None)
    if not plano:
        console.print("[bold red]Plano não encontrado.[/bold red]")
        return

    # 2. Chamar o MÉTODO DE NEGÓCIO (Troca de Plano)
    a.trocar_plano(novo_idp)

    # 3. Serializar e salvar de volta no repositório (Persistência)
    repo_assinaturas.update("id_assinatura", a.id_assinatura, a.to_dict())
    logger.info(f"Plano da assinatura {a.id_assinatura} trocado para {novo_idp}")
    console.print(f"[bold green]Plano alterado com sucesso para:[/bold green] [bold yellow]{plano['nome']}[/bold yellow]")


def cancelar_assinatura():
    ida = console.input("[yellow]ID da assinatura:[/yellow] ").strip()
    assinatura_data = repo_assinaturas.find_by_id("id_assinatura", ida)
    if not assinatura_data:
        console.print("[bold red]Assinatura não encontrada.[/bold red]")
        return

    # 1. Carregar o objeto para aplicar a regra de negócio
    a = Assinatura(**assinatura_data)

    try:
        # 2. Chamar o MÉTODO DE NEGÓCIO (Cancelamento)
        a.cancelar()

        # 3. Serializar e salvar de volta no repositório (Persistência)
        repo_assinaturas.update("id_assinatura", a.id_assinatura, a.to_dict())
        logger.info(f"Assinatura {a.id_assinatura} cancelada.")
        console.print("[bold green]Assinatura cancelada com sucesso.[/bold green]")
    except RuntimeError as e:
        console.print(f"[bold red]ERRO ao cancelar:[/bold red] {e}")


def registrar_pagamento():
    ida = console.input("[yellow]ID da assinatura:[/yellow] ").strip()
    assinatura_data = repo_assinaturas.find_by_id("id_assinatura", ida)
    if not assinatura_data:
        console.print("[bold red]Assinatura não encontrada.[/bold red]")
        return

    # 1. Pegar o valor do plano associado
    idp = assinatura_data['id_plano']
    plano_data = repo_planos.find_by_id("id_plano", idp)
    if not plano_data:
        console.print("[bold red]Plano associado não encontrado.[/bold red]")
        return
        
    valor_plano = plano_data['preco_mensal']
    
    # Coletar dados do pagamento
    metodo = console.input(f"[yellow]Método de pagamento (Valor: R${valor_plano:.2f}):[/yellow] ").strip()
    
    # 2. Criar objeto Pagamento (inicialmente 'pendente')
    id_pagamento = gerar_id("pgm")
    pagamento = Pagamento(id_pagamento, ida, valor_plano, metodo)

    try:
        # 3. Simular a confirmação (chama o MÉTODO DE NEGÓCIO: confirmar_pagamento)
        pagamento.confirmar_pagamento()
        
        # 4. Serializar e salvar no Repositório (Persistência)
        repo_pagamentos.insert(pagamento.to_dict())
        logger.info(f"Pagamento {id_pagamento} confirmado para assinatura {ida}.")
        
        console.print(f"[bold green]Pagamento de R${valor_plano:.2f} confirmado com sucesso.[/bold green]")
        
    except RuntimeError as e:
        console.print(f"[bold red]ERRO ao confirmar pagamento:[/bold red] {e}")


def listar_assinaturas():
    # Cria uma Tabela Rich para formatação visual
    table = Table(title="Lista de Assinaturas", show_header=True, header_style="bold yellow")
    table.add_column("ID", style="dim", width=12)
    table.add_column("Usuário ID")
    table.add_column("Plano ID")
    table.add_column("Status", style="bold")
    
    # Adiciona cor dinâmica baseada no Status
    for a in repo_assinaturas.list_all():
        status_color = "green" if a['status'] == "ativa" else "red" if a['status'] == "cancelada" else "yellow"
        table.add_row(a['id_assinatura'], a['id_usuario'], a['id_plano'], f"[{status_color}]{a['status']}[/{status_color}]")
        
    console.print(table)

# --- MENU PRINCIPAL (Interface do Usuário) ---
def menu():
    seed_planos() # Inicializa os dados
    while True:
        console.print("\n[bold blue]Menu Principal[/bold blue]")
        # Opções do menu
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
            # Chama a função de negócio correspondente à opção
            if op == "1": cadastrar_usuario()
            elif op == "2": excluir_usuario()
            elif op == "3": listar_usuarios()
            elif op == "4": criar_assinatura()
            elif op == "5": trocar_plano()
            elif op == "6": cancelar_assinatura()
            elif op == "7": registrar_pagamento() # <--- AGORA DEFINIDA CORRETAMENTE ACIMA
            elif op == "8": listar_assinaturas()
            elif op == "0": break
            else: console.print("[bold red]Opção inválida.[/bold red]")
        except Exception as e:
            # Tratamento de Exceção e Log de Erro
            logger.error(str(e))
            console.print(f"[bold red]ERRO:[/bold red] {e}")

# Início da Aplicação
if __name__ == "__main__":
    menu()