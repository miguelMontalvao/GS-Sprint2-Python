# pele_nextgen_validacao.py

from dataclasses import dataclass, field
from typing import Dict, Set, Tuple


# =========================
# MODELOS DE DOMÍNIO
# =========================

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
    videos: list = field(default_factory=list)
    avaliacoes: list = field(default_factory=list)

    def dados_publicos(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "posicao": self.posicao,
            "idade": self.idade,
            "nota_media": self.nota_media,
            "cidade": self.cidade
        }

    def dados_completos(self):
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
            "avaliacoes": self.avaliacoes
        }


@dataclass
class Clube:
    id: int
    nome: str


# =========================
# REGRA DE NEGÓCIO CENTRAL
# =========================

class PlataformaScouting:
    """
    Regra central validada:
    - Sem desbloqueio: clube vê apenas dados públicos do atleta.
    - Com desbloqueio: clube vê dados completos + avaliações + pode iniciar chat.
    - O desbloqueio é único e permanente por par (clube, atleta).
    """

    def __init__(self):
        # guarda pares (clube_id, atleta_id) desbloqueados
        self.desbloqueios: Set[Tuple[int, int]] = set()

    def desbloquear_contato(self, clube: Clube, atleta: Atleta) -> str:
        chave = (clube.id, atleta.id)

        if chave in self.desbloqueios:
            return (
                f"[INFO] O clube '{clube.nome}' já desbloqueou o atleta '{atleta.nome}'. "
                f"Desbloqueio é único e permanente."
            )

        self.desbloqueios.add(chave)
        return (
            f"[SUCESSO] Contato do atleta '{atleta.nome}' desbloqueado para o clube '{clube.nome}'."
        )

    def possui_desbloqueio(self, clube: Clube, atleta: Atleta) -> bool:
        return (clube.id, atleta.id) in self.desbloqueios

    def visualizar_perfil(self, clube: Clube, atleta: Atleta) -> dict:
        if self.possui_desbloqueio(clube, atleta):
            return atleta.dados_completos()
        return atleta.dados_publicos()

    def visualizar_avaliacoes(self, clube: Clube, atleta: Atleta):
        if self.possui_desbloqueio(clube, atleta):
            return atleta.avaliacoes
        raise PermissionError(
            f"O clube '{clube.nome}' não pode visualizar avaliações do atleta '{atleta.nome}' sem desbloqueio."
        )

    def iniciar_chat(self, clube: Clube, atleta: Atleta) -> str:
        if not self.possui_desbloqueio(clube, atleta):
            raise PermissionError(
                f"O clube '{clube.nome}' não pode iniciar chat com '{atleta.nome}' sem desbloqueio."
            )

        return f"[CHAT] Chat iniciado entre clube '{clube.nome}' e atleta '{atleta.nome}'."


# =========================
# TESTES DE VALIDAÇÃO
# =========================

def executar_testes():
    print("=" * 70)
    print("VALIDAÇÃO DA REGRA DE NEGÓCIO CENTRAL - PELÉ NEXT GEN")
    print("=" * 70)

    # Massa de dados
    atleta = Atleta(
        id=1,
        nome="João Silva",
        posicao="Meia",
        idade=18,
        nota_media=8.7,
        cidade="São Paulo",
        telefone="(11) 99999-9999",
        email="joao@atleta.com",
        videos=["video_gol.mp4", "video_assistencias.mp4"],
        avaliacoes=[
            {"atributo": "Velocidade", "nota": 8.5},
            {"atributo": "Passe", "nota": 9.0},
            {"atributo": "Finalização", "nota": 8.2}
        ]
    )

    clube = Clube(id=101, nome="Clube Atlético Futuro")

    sistema = PlataformaScouting()

    # -------------------------
    # TESTE 1: sem desbloqueio
    # -------------------------
    print("\n[TESTE 1] Clube SEM desbloqueio")
    perfil = sistema.visualizar_perfil(clube, atleta)
    print("Perfil retornado:", perfil)

    # Validação: deve conter só dados públicos
    assert "telefone" not in perfil, "ERRO: telefone não deveria aparecer sem desbloqueio"
    assert "email" not in perfil, "ERRO: email não deveria aparecer sem desbloqueio"
    assert "avaliacoes" not in perfil, "ERRO: avaliações não deveriam aparecer sem desbloqueio"
    print("[OK] Clube sem desbloqueio visualiza apenas dados públicos.")

    # Tentativa de ver avaliações
    try:
        sistema.visualizar_avaliacoes(clube, atleta)
        print("[ERRO] O clube não deveria visualizar avaliações sem desbloqueio.")
    except PermissionError as e:
        print("[OK]", e)

    # Tentativa de iniciar chat
    try:
        sistema.iniciar_chat(clube, atleta)
        print("[ERRO] O clube não deveria iniciar chat sem desbloqueio.")
    except PermissionError as e:
        print("[OK]", e)

    # -------------------------
    # TESTE 2: realizar desbloqueio
    # -------------------------
    print("\n[TESTE 2] Clube COM desbloqueio")
    print(sistema.desbloquear_contato(clube, atleta))

    perfil = sistema.visualizar_perfil(clube, atleta)
    print("Perfil retornado:", perfil)

    assert "telefone" in perfil, "ERRO: telefone deveria aparecer após desbloqueio"
    assert "email" in perfil, "ERRO: email deveria aparecer após desbloqueio"
    assert "avaliacoes" in perfil, "ERRO: avaliações deveriam aparecer após desbloqueio"
    print("[OK] Clube com desbloqueio visualiza dados completos.")

    avaliacoes = sistema.visualizar_avaliacoes(clube, atleta)
    assert len(avaliacoes) > 0, "ERRO: avaliações deveriam estar disponíveis após desbloqueio"
    print("[OK] Clube com desbloqueio visualiza avaliações:", avaliacoes)

    chat = sistema.iniciar_chat(clube, atleta)
    print("[OK]", chat)

    # -------------------------
    # TESTE 3: desbloqueio duplicado
    # -------------------------
    print("\n[TESTE 3] Tentativa de desbloqueio duplicado")
    msg = sistema.desbloquear_contato(clube, atleta)
    print(msg)
    assert "já desbloqueou" in msg, "ERRO: o sistema deveria impedir/descrever desbloqueio duplicado"
    print("[OK] Regra de desbloqueio único validada.")

    print("\n" + "=" * 70)
    print("RESULTADO FINAL: TODAS AS VALIDAÇÕES DA REGRA CENTRAL PASSARAM.")
    print("=" * 70)


if __name__ == "__main__":
    executar_testes()