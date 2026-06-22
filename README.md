Feito por: Julio Cesar Junior (570047),
Miguel Menezes (573825),
Pedro Provadelli (572547),
Arthur Moreira (571532) e
Vitor Louzano (573885)

O script foi desenvolvido com base na seguinte regra de negócio central :

A regra de negócio central da plataforma Pelé Next Gen é o desbloqueio de contato entre clube e atleta, 
pois ele controla a transição entre visualização pública e acesso completo ao atleta, além de habilitar avaliações e comunicação via chat.

# ⚽ Pelé Next Gen — Validação da Regra de Negócio Central

> Script Python de validação da plataforma de peneiras digitais Pelé Next Gen, executado em terminal/console.

---

## Visão Geral

`pele_nextgen_validacao.py` é um script interativo que implementa e valida a **regra de negócio central** da plataforma Pelé Next Gen: o controle de acesso a dados de atletas via desbloqueio de contato. O programa simula os módulos de busca, perfil, avaliações e chat, aplicando as restrições de acesso diretamente no código.

O script foi estruturado com base nos seguintes pilares técnicos:

| # | Requisito |
|---|-----------|
| 1 | Armazenamento de dados em listas e dicionários |
| 2 | Análise via matrizes e laços de repetição |
| 3 | Regras de negócio implementadas com estruturas condicionais |
| 4 | Código organizado em funções para manutenção e reutilização |
| 5 | Interatividade via `input()` e menu com laço `while` |

---

## Regra de Negócio Central — Desbloqueio de Contato

O **desbloqueio de contato** é o núcleo do sistema. Ele controla a transição entre visualização pública e acesso completo ao atleta, além de habilitar avaliações e chat.

### Fluxo implementado

```
[Clube busca atleta]
        │
        ▼
[Visualiza dados públicos resumidos]
  nome, posição, idade, nota_media, cidade
        │
        ▼
[Clube solicita desbloqueio]
  desbloquear_contato(clube, atleta)
        │
        ▼
[Acesso permanente liberado — par (clube_id, atleta_id) gravado em Set]
        │
        ├─► perfil completo  → visualizar_perfil()
        ├─► avaliações       → visualizar_avaliacoes()
        └─► chat             → iniciar_chat()
```

### Regras do Desbloqueio (RN-14 a RN-17)

- **RN-14** — Acesso a dados completos, avaliações e chat exige desbloqueio prévio.
- **RN-15** — O desbloqueio é **único e permanente** por par `(clube_id, atleta_id)` — armazenado em um `Set[Tuple[int, int]]`; tentativas repetidas retornam aviso sem novo registro.
- **RN-16** — **Sem desbloqueio:** `visualizar_perfil()` retorna apenas `dados_publicos()` — nome, posição, idade, nota média e cidade.
- **RN-17** — **Com desbloqueio:** `visualizar_perfil()` retorna `dados_completos()` — acrescenta telefone, e-mail, vídeos e avaliações.

### Regras do Chat (RN-18 a RN-22)

- **RN-18** — `iniciar_chat()` lança `RegraDeNegocioError` se não houver desbloqueio para o par.
- **RN-19** — A iniciativa do chat é exclusiva do clube (chamada sempre parte do lado clube).
- **RN-20** — Após desbloqueio confirmado, o canal é habilitado e a mensagem de sucesso é retornada.
- **RN-21** — O vínculo chat ↔ par `(clube, atleta)` é garantido pela chave do desbloqueio.
- **RN-22** — Tentativas sem desbloqueio são bloqueadas por exceção tipada (`RegraDeNegocioError`).

---

## Estrutura do Código

```
pele_nextgen_validacao.py
│
├── Modelos de Domínio
│   ├── Atleta          # dados_publicos() / dados_completos()
│   └── Clube
│
├── Exceção
│   └── RegraDeNegocioError
│
├── Camada de Negócio
│   └── PlataformaScouting
│       ├── possui_desbloqueio()
│       ├── desbloquear_contato()    ← regra central
│       ├── visualizar_perfil()
│       ├── visualizar_avaliacoes()
│       ├── iniciar_chat()
│       ├── gerar_matriz_atletas()
│       ├── classificar_talento()
│       └── calcular_media_geral()
│
├── Funções de UI / Menu
│   ├── cadastrar_atleta()
│   ├── cadastrar_clube()
│   ├── listar_atletas() / listar_clubes()
│   ├── buscar_atletas_por_filtros()
│   ├── desbloquear_contato_menu()
│   ├── visualizar_perfil_menu()
│   ├── visualizar_avaliacoes_menu()
│   ├── iniciar_chat_menu()
│   ├── exibir_matriz_atletas()
│   ├── exibir_media_geral()
│   └── carregar_dados_exemplo()
│
└── Execução
    └── menu_principal()
```

---

## Menu Interativo

Ao executar o script, o usuário acessa um menu com as seguintes opções:

| Opção | Ação |
|-------|------|
| `1` | Cadastrar atleta |
| `2` | Cadastrar clube |
| `3` | Listar atletas |
| `4` | Listar clubes |
| `5` | Buscar atletas por filtros (posição, idade, nota, cidade) |
| `6` | **Desbloquear contato** de atleta ← regra central |
| `7` | Visualizar perfil de atleta (resumido ou completo) |
| `8` | Visualizar avaliações (exige desbloqueio) |
| `9` | Iniciar chat com atleta (exige desbloqueio) |
| `10` | Exibir matriz de atletas |
| `11` | Exibir média geral dos atletas |
| `12` | Carregar dados de exemplo |
| `0` | Sair |

---

## Classificação de Talentos

A função `classificar_talento()` categoriza atletas com base na nota média:

| Nota Média | Status |
|-----------|--------|
| ≥ 8.5 | `APROVADO` |
| ≥ 7.0 | `EM OBSERVAÇÃO` |
| < 7.0 | `REPROVADO` |

---

## Como Executar

**Pré-requisito:** Python 3.7 ou superior (uso de `dataclasses`).

```bash
# Clone o repositório
git clone https://github.com/seu-org/pele-next-gen.git
cd pele-next-gen

# Execute o script
python pele_nextgen_validacao.py
```

Para uma demonstração rápida, escolha a opção `12` no menu para carregar os dados de exemplo pré-configurados (3 atletas e 2 clubes).

---

<p align="center">Feito com ⚽ pela equipe Pelé Next Gen</p>
