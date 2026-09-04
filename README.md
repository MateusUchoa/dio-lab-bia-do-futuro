# 🤖 Agente Financeiro Inteligente com IA Generativa

## Contexto

O Êxodo Bot é um agente de Inteligência Artificial criado para guiar investidores iniciantes para fora do "deserto da ignorância" rumo à autonomia financeira, rodando 100% localmente. Desenvolvido para o desafio de Agentes de IA da DIO, ele atua como um mentor educacional que utiliza uma base de conhecimento restrita (RAG) e regras estritas de compliance para ensinar sobre o mercado sem realizar recomendações diretas de ativos:

-Principais Funcionalidades e Diferenciais
Privacidade e Execução Local: O motor LLM roda na própria máquina utilizando Ollama, garantindo que os dados do usuário não sejam enviados para APIs externas.

-Travas de Segurança (Anti-Alucinação): Regras inegociáveis no System Prompt bloqueiam recomendações de compra/venda, promessas de rentabilidade e assuntos fora do escopo (como criptomoedas).

-Roteamento Dinâmico de Contexto: O sistema analisa a pergunta do usuário e injeta apenas os documentos relevantes (JSON) no prompt, economizando tokens e focando a resposta.

---

### 1. Documentação do Agente
Arquitetura e Tecnologias
Componente        Tecnologia            Propósito
Interface (UI)    StreamlitChat         interativo fluido com suporte a respostas em streaming.
Motor LLM         Ollama                Orquestração e execução local de grandes modelos de linguagem.
Modelo Base       Qwen2.5-coder:14b     Raciocínio lógico, extração de contexto e formatação de texto em português.
Back-end e RAG    Python 3              Lógica de correspondência de palavras-chave para injeção de contexto.

---

### 2. Base de Conhecimento

Os dados mockados que alimentam as respostas do agente estão estruturados em arquivos JSON focados em literatura consagrada e regras oficiais:
Arquivo JSON                        Conteúdo Base                                    Palavras-chave de Ativação
CVM_bolsa.json                      Diretrizes, regras e prevenção a fraudes.        cvm, regra, fraude, regulamentação
glossario_b3.json                   Termos e jargões da Bolsa de Valores.            o que é, ação, fii, dividendo, etf
produtos_financeiros.json           Explicação sobre classes de ativos.              renda fixa, tesouro, cdb, fundo
investidor_inteligente.json         Filosofia de Benjamin Graham (Value Investing).  margem de segurança, valor intrínseco
mil_ao_milhao.json                  Pilares da riqueza (Thiago Nigro).               poupar, rentabilidade, gastos

---

### 3. Aplicação Funcional

Como Executar o Projeto Localmente
Pré-requisitos: Instale o Ollama no seu computador.

Baixe o modelo LLM: Abra o terminal e execute o comando de download do modelo escolhido:

Bash
ollama run qwen2.5-coder:14b
Clone este repositório e instale as bibliotecas:

Bash
pip install streamlit ollama
Inicie a interface: No diretório do projeto, rode o comando:

Bash
streamlit run app.py

---

## Estrutura do Repositório

```
📁 exodo-bot-agente-financeiro/
│
├── 📄 README.md                 # Documentação principal
├── 📄 Êxodo_bot.py              # Código-fonte principal (Streamlit + Ollama + Métricas)
|
│
├── 📁 data/                     # Base de Conhecimento RAG
│   ├── CVM_bolsa.json
│   ├── glossario_b3_base.json
│   ├── produtos_financeiros.json
│   ├── perfil_investidor.json
│   ├── json_investidor_inteligente.json
│   └── json_mil_ao_milhao.json
│
└── 📁 docs/                     # Documentação de apoio do desafio DIO
    ├── 01-documentacao-agente.md
    ├── 02-base-conhecimento.md
    ├── 03-prompts.md
    └── 05-pitch.md```
