"""
pele_nextgen_validacao.py

Script desenvolvido para validar a regra de negócio central da solução
proposta para a Pelé Academia (Pelé Next Gen), executado em terminal/console.

O programa foi estruturado para atender aos requisitos da atividade:

1. Utilização de listas e dicionários para armazenamento dos dados.
2. Manipulação e análise dos dados utilizando matrizes e laços de repetição.
3. Implementação das regras de negócio por meio de estruturas condicionais.
4. Organização do código em funções para facilitar a manutenção e reutilização.
5. Interatividade com o usuário através de um menu principal utilizando
   a função input() e um laço while.

Regra de negócio central validada:
- Um clube só pode acessar os dados completos de um atleta, visualizar
  avaliações privadas e iniciar um chat após realizar o desbloqueio do
  contato desse atleta.
- O desbloqueio é único e permanente para cada par (clube, atleta).

"""

from dataclasses import dataclass, field
from typing import List, Dict, Set, Tuple, Optional


# ============================================================
# MODELOS DE DOMÍNIO
# ============================================================

@dataclass
class Atleta:
    id: int
    nome: str
    posicao: str
    idade: int
    nota_media: float
    cidade: str
    telefone: str
    email: str
    videos: List[str] = field(default_factory=list)
    avaliacoes: List[Dict] = field(default_factory=list)

    def dados_publicos(self) -> Dict:
        """Dados visíveis para qualquer clube sem desbloqueio."""
        return {
            "id": self.id,
            "nome": self.nome,
            "posicao": self.posicao,
            "idade": self.idade,
            "nota_media": self.nota_media,
            "cidade": self.cidade,
        }

    def dados_completos(self) -> Dict:
        """Dados liberados após desbloqueio."""
        return {
            "id": self.id,
            "nome": self.nome,
            "posicao": self.posicao,
            "idade": self.idade,
            "nota_media": self.nota_media,
            "cidade": self.cidade,
            "telefone": self.telefone,
            "email": self.email,
            "videos": self.videos,
            "avaliacoes": self.avaliacoes,
        }


@dataclass
class Clube:
    id: int
    nome: str


# ============================================================
# EXCEÇÃO DE REGRA DE NEGÓCIO
# ============================================================

class RegraDeNegocioError(Exception):
    """Erro específico de regra de negócio."""
    pass


# ============================================================
# CAMADA DE NEGÓCIO / SISTEMA
# ============================================================

class PlataformaScouting:
    """
    Regra de negócio central:
    1) Sem desbloqueio: clube vê apenas dados públicos do atleta.
    2) Com desbloqueio: clube vê dados completos, avaliações e pode iniciar chat.
    3) O desbloqueio é único e permanente por par (clube, atleta).
    """

    def __init__(self):
        # Requisito 1: armazenamento estruturado em memória
        self.atletas: List[Atleta] = []
        self.clubes: List[Clube] = []

        # Estrutura para regra de desbloqueio
        self.desbloqueios: Set[Tuple[int, int]] = set()

    # ========================================================
    # CADASTROS / ARMAZENAMENTO
    # ========================================================

    def adicionar_atleta(self, atleta: Atleta) -> None:
        self.atletas.append(atleta)

    def adicionar_clube(self, clube: Clube) -> None:
        self.clubes.append(clube)

    def buscar_atleta_por_id(self, atleta_id: int) -> Optional[Atleta]:
        for atleta in self.atletas:
            if atleta.id == atleta_id:
                return atleta
        return None

    def buscar_clube_por_id(self, clube_id: int) -> Optional[Clube]:
        for clube in self.clubes:
            if clube.id == clube_id:
                return clube
        return None

    # ========================================================
    # REGRA DE NEGÓCIO CENTRAL
    # ========================================================

    def possui_desbloqueio(self, clube: Clube, atleta: Atleta) -> bool:
        return (clube.id, atleta.id) in self.desbloqueios

    def desbloquear_contato(self, clube: Clube, atleta: Atleta) -> str:
        chave = (clube.id, atleta.id)

        if chave in self.desbloqueios:
            return (
                f"[INFO] O clube '{clube.nome}' já desbloqueou o atleta "
                f"'{atleta.nome}'. O desbloqueio é único e permanente."
            )

        self.desbloqueios.add(chave)
        return (
            f"[SUCESSO] Contato do atleta '{atleta.nome}' desbloqueado "
            f"para o clube '{clube.nome}'."
        )

    def visualizar_perfil(self, clube: Clube, atleta: Atleta) -> Dict:
        if self.possui_desbloqueio(clube, atleta):
            return atleta.dados_completos()
        return atleta.dados_publicos()

    def visualizar_avaliacoes(self, clube: Clube, atleta: Atleta) -> List[Dict]:
        if not self.possui_desbloqueio(clube, atleta):
            raise RegraDeNegocioError(
                f"O clube '{clube.nome}' não pode visualizar avaliações do "
                f"atleta '{atleta.nome}' sem desbloqueio."
            )
        return atleta.avaliacoes

    def iniciar_chat(self, clube: Clube, atleta: Atleta) -> str:
        if not self.possui_desbloqueio(clube, atleta):
            raise RegraDeNegocioError(
                f"O clube '{clube.nome}' não pode iniciar chat com "
                f"'{atleta.nome}' sem desbloqueio."
            )
        return f"[CHAT] Chat iniciado entre '{clube.nome}' e '{atleta.nome}'."

    # ========================================================
    # ANÁLISE / MATRIZ / PROCESSAMENTO
    # ========================================================

    def gerar_matriz_atletas(self) -> List[List]:
        """
        Requisito 2:
        Retorna uma matriz (lista de listas) com dados tabulados dos atletas.
        """
        matriz = [["ID", "Nome", "Posição", "Idade", "Nota Média", "Cidade", "Status"]]

        for atleta in self.atletas:
            status = self.classificar_talento(atleta.nota_media)
            matriz.append([
                atleta.id,
                atleta.nome,
                atleta.posicao,
                atleta.idade,
                atleta.nota_media,
                atleta.cidade,
                status
            ])
        return matriz

    def classificar_talento(self, nota_media: float) -> str:
        """
        Requisito 3:
        Exemplo de decisão com if/elif/else para aprovar/reprovar um talento.
        """
        if nota_media >= 8.5:
            return "APROVADO"
        elif nota_media >= 7.0:
            return "EM OBSERVAÇÃO"
        else:
            return "REPROVADO"

    def calcular_media_geral(self) -> float:
        if not self.atletas:
            return 0.0

        soma = 0.0
        for atleta in self.atletas:
            soma += atleta.nota_media
        return soma / len(self.atletas)


# ============================================================
# FUNÇÕES DE APOIO / UI
# ============================================================

def imprimir_titulo() -> None:
    print("=" * 78)
    print("PELÉ NEXT GEN - VALIDAÇÃO DA REGRA DE NEGÓCIO CENTRAL".center(78))
    print("=" * 78)


def imprimir_menu() -> None:
    print("\nMENU PRINCIPAL")
    print("1 - Cadastrar atleta")
    print("2 - Cadastrar clube")
    print("3 - Listar atletas")
    print("4 - Listar clubes")
    print("5 - Buscar atletas por filtros")
    print("6 - Desbloquear contato de atleta")
    print("7 - Visualizar perfil de atleta")
    print("8 - Visualizar avaliações de atleta")
    print("9 - Iniciar chat com atleta")
    print("10 - Exibir matriz de atletas")
    print("11 - Exibir média geral dos atletas")
    print("12 - Carregar dados de exemplo")
    print("0 - Sair")


def ler_int(mensagem: str) -> int:
    while True:
        try:
            return int(input(mensagem))
        except ValueError:
            print("[ERRO] Digite um número inteiro válido.")


def ler_float(mensagem: str) -> float:
    while True:
        try:
            return float(input(mensagem))
        except ValueError:
            print("[ERRO] Digite um número decimal válido.")


def cadastrar_atleta(sistema: PlataformaScouting) -> None:
    print("\n=== CADASTRO DE ATLETA ===")
    atleta_id = ler_int("ID do atleta: ")

    if sistema.buscar_atleta_por_id(atleta_id):
        print("[ERRO] Já existe um atleta com esse ID.")
        return

    nome = input("Nome: ").strip()
    posicao = input("Posição: ").strip()
    idade = ler_int("Idade: ")
    nota_media = ler_float("Nota média: ")
    cidade = input("Cidade: ").strip()
    telefone = input("Telefone: ").strip()
    email = input("Email: ").strip()

    videos: List[str] = []
    avaliacoes: List[Dict] = []

    qtd_videos = ler_int("Quantidade de vídeos para cadastrar: ")
    for i in range(qtd_videos):
        video = input(f"Vídeo {i + 1}: ").strip()
        videos.append(video)

    qtd_avaliacoes = ler_int("Quantidade de avaliações para cadastrar: ")
    for i in range(qtd_avaliacoes):
        atributo = input(f"Atributo da avaliação {i + 1}: ").strip()
        nota = ler_float(f"Nota do atributo '{atributo}': ")
        avaliacoes.append({
            "atributo": atributo,
            "nota": nota
        })

    atleta = Atleta(
        id=atleta_id,
        nome=nome,
        posicao=posicao,
        idade=idade,
        nota_media=nota_media,
        cidade=cidade,
        telefone=telefone,
        email=email,
        videos=videos,
        avaliacoes=avaliacoes,
    )

    sistema.adicionar_atleta(atleta)
    print(f"[SUCESSO] Atleta '{nome}' cadastrado com sucesso.")


def cadastrar_clube(sistema: PlataformaScouting) -> None:
    print("\n=== CADASTRO DE CLUBE ===")
    clube_id = ler_int("ID do clube: ")

    if sistema.buscar_clube_por_id(clube_id):
        print("[ERRO] Já existe um clube com esse ID.")
        return

    nome = input("Nome do clube: ").strip()
    clube = Clube(id=clube_id, nome=nome)
    sistema.adicionar_clube(clube)

    print(f"[SUCESSO] Clube '{nome}' cadastrado com sucesso.")


def listar_atletas(sistema: PlataformaScouting) -> None:
    print("\n=== LISTA DE ATLETAS ===")
    if not sistema.atletas:
        print("[INFO] Nenhum atleta cadastrado.")
        return

    for atleta in sistema.atletas:
        status = sistema.classificar_talento(atleta.nota_media)
        print(
            f"ID: {atleta.id} | Nome: {atleta.nome} | Posição: {atleta.posicao} | "
            f"Idade: {atleta.idade} | Nota: {atleta.nota_media:.1f} | "
            f"Cidade: {atleta.cidade} | Status: {status}"
        )


def listar_clubes(sistema: PlataformaScouting) -> None:
    print("\n=== LISTA DE CLUBES ===")
    if not sistema.clubes:
        print("[INFO] Nenhum clube cadastrado.")
        return

    for clube in sistema.clubes:
        print(f"ID: {clube.id} | Nome: {clube.nome}")


def buscar_atletas_por_filtros(sistema: PlataformaScouting) -> None:
    """
    Demonstra uso de laços + condicionais para filtrar dados.
    """
    print("\n=== BUSCA DE ATLETAS POR FILTROS ===")
    if not sistema.atletas:
        print("[INFO] Nenhum atleta cadastrado.")
        return

    posicao = input("Filtrar por posição (ou deixe vazio): ").strip().lower()
    idade_max = input("Idade máxima (ou deixe vazio): ").strip()
    nota_min = input("Nota mínima (ou deixe vazio): ").strip()
    cidade = input("Cidade (ou deixe vazio): ").strip().lower()

    idade_max_valor = int(idade_max) if idade_max else None
    nota_min_valor = float(nota_min) if nota_min else None

    encontrados = []

    for atleta in sistema.atletas:
        if posicao and atleta.posicao.lower() != posicao:
            continue
        if idade_max_valor is not None and atleta.idade > idade_max_valor:
            continue
        if nota_min_valor is not None and atleta.nota_media < nota_min_valor:
            continue
        if cidade and atleta.cidade.lower() != cidade:
            continue

        encontrados.append(atleta)

    if not encontrados:
        print("[INFO] Nenhum atleta encontrado com esses filtros.")
        return

    print("\nAtletas encontrados:")
    for atleta in encontrados:
        print(
            f"- ID {atleta.id} | {atleta.nome} | {atleta.posicao} | "
            f"Idade {atleta.id} | Nota {atleta.nota_media:.1f} | {atleta.cidade}"
        )


def selecionar_clube_e_atleta(sistema: PlataformaScouting) -> Tuple[Optional[Clube], Optional[Atleta]]:
    if not sistema.clubes:
        print("[ERRO] Não há clubes cadastrados.")
        return None, None

    if not sistema.atletas:
        print("[ERRO] Não há atletas cadastrados.")
        return None, None

    clube_id = ler_int("Informe o ID do clube: ")
    atleta_id = ler_int("Informe o ID do atleta: ")

    clube = sistema.buscar_clube_por_id(clube_id)
    atleta = sistema.buscar_atleta_por_id(atleta_id)

    if not clube:
        print("[ERRO] Clube não encontrado.")
        return None, None

    if not atleta:
        print("[ERRO] Atleta não encontrado.")
        return None, None

    return clube, atleta


def desbloquear_contato_menu(sistema: PlataformaScouting) -> None:
    print("\n=== DESBLOQUEAR CONTATO ===")
    clube, atleta = selecionar_clube_e_atleta(sistema)
    if clube and atleta:
        print(sistema.desbloquear_contato(clube, atleta))


def visualizar_perfil_menu(sistema: PlataformaScouting) -> None:
    print("\n=== VISUALIZAR PERFIL DE ATLETA ===")
    clube, atleta = selecionar_clube_e_atleta(sistema)
    if clube and atleta:
        perfil = sistema.visualizar_perfil(clube, atleta)
        print("\nPerfil retornado:")
        for chave, valor in perfil.items():
            print(f"{chave}: {valor}")


def visualizar_avaliacoes_menu(sistema: PlataformaScouting) -> None:
    print("\n=== VISUALIZAR AVALIAÇÕES ===")
    clube, atleta = selecionar_clube_e_atleta(sistema)
    if clube and atleta:
        try:
            avaliacoes = sistema.visualizar_avaliacoes(clube, atleta)
            print(f"\nAvaliações de {atleta.nome}:")
            for avaliacao in avaliacoes:
                print(f"- {avaliacao['atributo']}: {avaliacao['nota']}")
        except RegraDeNegocioError as erro:
            print(f"[ERRO] {erro}")


def iniciar_chat_menu(sistema: PlataformaScouting) -> None:
    print("\n=== INICIAR CHAT ===")
    clube, atleta = selecionar_clube_e_atleta(sistema)
    if clube and atleta:
        try:
            mensagem = sistema.iniciar_chat(clube, atleta)
            print(mensagem)
        except RegraDeNegocioError as erro:
            print(f"[ERRO] {erro}")


def exibir_matriz_atletas(sistema: PlataformaScouting) -> None:
    """
    Requisito 2:
    Exibe uma matriz (lista de listas) e a percorre com laços.
    """
    print("\n=== MATRIZ DE ATLETAS ===")
    matriz = sistema.gerar_matriz_atletas()

    if len(matriz) == 1:
        print("[INFO] Nenhum atleta cadastrado.")
        return

    for linha in matriz:
        print(" | ".join(str(coluna) for coluna in linha))


def exibir_media_geral(sistema: PlataformaScouting) -> None:
    print("\n=== MÉDIA GERAL DOS ATLETAS ===")
    media = sistema.calcular_media_geral()
    print(f"Média geral: {media:.2f}")


def carregar_dados_exemplo(sistema: PlataformaScouting) -> None:
    """
    Carrega dados iniciais para facilitar demonstração e testes.
    """
    if sistema.atletas or sistema.clubes:
        print("[INFO] Já existem dados carregados no sistema.")
        return

    atleta1 = Atleta(
        id=1,
        nome="João Silva",
        posicao="Meia",
        idade=18,
        nota_media=8.7,
        cidade="São Paulo",
        telefone="(11) 99999-9999",
        email="joao@atleta.com",
        videos=["melhores_momentos.mp4", "assistencias.mp4"],
        avaliacoes=[
            {"atributo": "Velocidade", "nota": 8.5},
            {"atributo": "Passe", "nota": 9.0},
            {"atributo": "Finalização", "nota": 8.2},
        ],
    )

    atleta2 = Atleta(
        id=2,
        nome="Pedro Lima",
        posicao="Atacante",
        idade=17,
        nota_media=7.8,
        cidade="Rio de Janeiro",
        telefone="(21) 98888-7777",
        email="pedro@atleta.com",
        videos=["gols.mp4"],
        avaliacoes=[
            {"atributo": "Finalização", "nota": 8.4},
            {"atributo": "Velocidade", "nota": 7.6},
        ],
    )

    atleta3 = Atleta(
        id=3,
        nome="Carlos Souza",
        posicao="Zagueiro",
        idade=19,
        nota_media=6.4,
        cidade="Belo Horizonte",
        telefone="(31) 97777-1111",
        email="carlos@atleta.com",
        videos=["desarmes.mp4"],
        avaliacoes=[
            {"atributo": "Marcação", "nota": 6.8},
            {"atributo": "Impulsão", "nota": 6.0},
        ],
    )

    clube1 = Clube(id=101, nome="Clube Atlético Futuro")
    clube2 = Clube(id=102, nome="União FC")

    sistema.adicionar_atleta(atleta1)
    sistema.adicionar_atleta(atleta2)
    sistema.adicionar_atleta(atleta3)
    sistema.adicionar_clube(clube1)
    sistema.adicionar_clube(clube2)

    print("[SUCESSO] Dados de exemplo carregados com sucesso.")


# ============================================================
# MENU PRINCIPAL
# ============================================================

def menu_principal() -> None:
    sistema = PlataformaScouting()

    imprimir_titulo()

    while True:
        imprimir_menu()
        opcao = input("\nEscolha uma opção: ").strip()

        if opcao == "1":
            cadastrar_atleta(sistema)

        elif opcao == "2":
            cadastrar_clube(sistema)

        elif opcao == "3":
            listar_atletas(sistema)

        elif opcao == "4":
            listar_clubes(sistema)

        elif opcao == "5":
            buscar_atletas_por_filtros(sistema)

        elif opcao == "6":
            desbloquear_contato_menu(sistema)

        elif opcao == "7":
            visualizar_perfil_menu(sistema)

        elif opcao == "8":
            visualizar_avaliacoes_menu(sistema)

        elif opcao == "9":
            iniciar_chat_menu(sistema)

        elif opcao == "10":
            exibir_matriz_atletas(sistema)

        elif opcao == "11":
            exibir_media_geral(sistema)

        elif opcao == "12":
            carregar_dados_exemplo(sistema)

        elif opcao == "0":
            print("\nEncerrando o sistema...")
            print("Obrigado por utilizar a validação da Pelé Next Gen.")
            break

        else:
            print("[ERRO] Opção inválida. Tente novamente.")


# ============================================================
# EXECUÇÃO
# ============================================================

if __name__ == "__main__":
    menu_principal()
