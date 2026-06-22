Feito por: Julio Cesar Junior (570047),
Miguel Menezes (573825),
Pedro Provadelli (572547),
Arthur Moreira (571532) e
Vitor Louzano (573885)

O script foi desenvolvido com base na seguinte regra de negócio central :

A regra de negócio central da plataforma Pelé Next Gen é o desbloqueio de contato entre clube e atleta, 
pois ele controla a transição entre visualização pública e acesso completo ao atleta, além de habilitar avaliações e comunicação via chat.

# ⚽ Pelé Next Gen — Plataforma de Peneiras Digitais

> Conectando clubes e atletas de forma inteligente, transparente e segura.

---

## Visão Geral

**Pelé Next Gen** é uma plataforma digital de peneiras que digitaliza e estrutura o processo de descoberta e contratação de atletas. Clubes e olheiros podem buscar talentos com base em critérios técnicos, visualizar perfis públicos e, após o desbloqueio de contato, acessar dados completos, avaliações detalhadas e iniciar negociações via chat integrado.

A plataforma integra quatro módulos principais:

| Módulo | Descrição |
|--------|-----------|
| 🔍 **Busca** | Pesquisa de atletas por posição, idade, localização e outros filtros |
| 👤 **Perfil** | Dados públicos resumidos e perfil completo (pós-desbloqueio) |
| ⭐ **Avaliações** | Sistema de notas e feedbacks técnicos por parte dos clubes |
| 💬 **Chat** | Canal de comunicação direta entre clube e atleta |

---

## Regra de Negócio Central — Desbloqueio de Contato

O **desbloqueio de contato** é a regra mais importante da plataforma. Ele controla a transição entre a visualização pública de um atleta e o acesso completo ao seu perfil, além de habilitar avaliações e a comunicação via chat.

### Como funciona

```
[Clube busca atleta]
        │
        ▼
[Visualiza dados públicos resumidos]
        │
        ▼
[Clube solicita desbloqueio do atleta]
        │
        ▼
[Acesso permanente liberado para o par (Clube ↔ Atleta)]
        │
        ├─► Perfil completo
        ├─► Avaliações
        └─► Chat / Negociação
```

### Regras do Desbloqueio (RN-14 a RN-17)

- **RN-14** — Um clube somente pode acessar os dados completos de um atleta após realizar o desbloqueio desse atleta.
- **RN-15** — O desbloqueio é **único por par (clube, atleta)**: uma vez realizado, não pode ser desfeito nem repetido.
- **RN-16** — **Sem desbloqueio:** o clube visualiza apenas os dados públicos resumidos do atleta.
- **RN-17** — **Com desbloqueio:** o clube obtém acesso completo ao perfil, histórico, avaliações e chat.

### Regras do Chat (RN-18 a RN-22)

- **RN-18** — O canal de chat entre clube e atleta só é habilitado após o desbloqueio.
- **RN-19** — A iniciativa de contato via chat é exclusiva do clube (pós-desbloqueio).
- **RN-20** — O atleta pode responder e interagir no chat assim que o clube iniciar a conversa.
- **RN-21** — O histórico de chat é preservado e vinculado ao par (clube, atleta).
- **RN-22** — Tentativas de acesso ao chat sem desbloqueio prévio são bloqueadas pelo sistema.

---

## Módulos e Funcionalidades

### 🔍 Busca de Atletas
- Filtros por posição, idade, localização, nível e experiência
- Resultados exibem apenas dados públicos resumidos
- Clube pode marcar atletas para desbloqueio a partir dos resultados

### 👤 Perfil do Atleta

| Sem Desbloqueio | Com Desbloqueio |
|-----------------|-----------------|
| Nome e foto | Dados pessoais completos |
| Posição e idade | Histórico de clubes |
| Localização | Documentação e contatos |
| Estatísticas básicas | Avaliações recebidas |
| — | Acesso ao chat |

### ⭐ Avaliações
- Disponíveis somente para clubes que realizaram o desbloqueio
- Clubes podem registrar avaliações técnicas por atleta
- O atleta pode visualizar as avaliações recebidas

### 💬 Chat
- Habilitado exclusivamente após desbloqueio confirmado
- Canal persistente e vinculado ao par (clube, atleta)
- Suporte a negociações e comunicações formais

---

## Arquitetura de Alto Nível

```
┌──────────────────────────────────────────────────────────┐
│                     Pelé Next Gen                        │
│                                                          │
│  ┌─────────┐   ┌─────────┐   ┌────────────┐  ┌──────┐    │
│  │  Busca  │──►│  Perfil │──►│Desbloqueio │─►│ Chat │    │
│  └─────────┘   └─────────┘   └────────────┘  └──────┘    │
│                                     │                    │
│                               ┌─────▼─────┐              │
│                               │ Avaliações│              │
│                               └───────────┘              │
└──────────────────────────────────────────────────────────┘
```

---

## Como Executar Localmente

```bash
# Clone o repositório
git clone https://github.com/seu-org/pele-next-gen.git
cd pele-next-gen

# Instale as dependências
npm install   # ou yarn / pnpm

# Configure as variáveis de ambiente
cp .env.example .env

# Execute em modo de desenvolvimento
npm run dev
```







---

<p align="center">Feito com ⚽ pela equipe Pelé Next Gen</p>
