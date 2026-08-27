# Base de Conhecimento

## Dados Utilizados

Descreva se usou os arquivos da pasta `data`, por exemplo:

| Arquivo | Formato | Utilização no Agente |
|---------|---------|---------------------|
| `historico_atendimento.csv` | CSV | Contextualizar interações anteriores |
| `perfil_investidor.json` | JSON | Personalizar recomendações |
| `produtos_financeiros.json` | JSON | Sugerir produtos adequados ao perfil |
| `glossario_b3_base.json` | JSON | Glossário de termos da bolsa de valores |
| `json_investidor_inteligente.json` | JSON | Manual do investidor consultar para dar dicas de como escolher ações e fundo da bolsa de valores |
| `CVM_bolsa.json` | JSON | Guia CVM do Investidor: Como Funciona a Bolsa de Valores |
| `jovens_na_bolsa.json` | JSON | Dicas essenciais para começar a investir |
| `resumo json _mil_ao_milhão.json` | JSON | guia iniciantes na Bolsa ensinando a gastar bem, investir com foco no longo prazo e aportar com constância, priorizando a segurança e a educação financeira |

---

## Adaptações nos Dados

> Você modificou ou expandiu os dados mockados? Descreva aqui.

Foram adicionados mais arquivos em formato json para deixar a base de conhecimento do agente mais robusta e resumo publico de livros com  dicas práticas de como investir.

---

## Estratégia de Integração

### Como os dados são carregados?
> Descreva como seu agente acessa a base de conhecimento.

Os arquivos da base de conhecimento (JSON contendo o perfil do cliente, produtos disponíveis, livros/guias financeiros e glossário da B3) são lidos no início do pipeline da sessão e disponibilizados em memória. Eles são recuperados e estruturados para compor as diretrizes operacionais e os contextos específicos do agente.

### Como os dados são usados no prompt?
> Os dados vão no system prompt? São consultados dinamicamente?

Os dados são divididos em dois níveis:

System Prompt: Recebe regras gerais, metodologias de análise (ex: margem de segurança, três pilares da prosperidade) e parâmetros rígidos de conformidade/segurança.

Contexto Dinâmico (User Prompt / Context Ingestion): Injeta apenas as variáveis específicas do cliente atual (ex: perfil, renda, metas) e a fatia relevante dos produtos de investimento/regras de mercado no momento da interação, garantindo precisão sem sobrecarregar a janela de contexto.

---

## Exemplo de Contexto Montado

> Mostre um exemplo de como os dados são formatados para o agente.

```
**Estratégia de Integração**

**Como os dados são carregados?**
Os arquivos da base de conhecimento (JSON contendo o perfil do cliente, produtos disponíveis, livros/guias financeiros e glossário da B3) são lidos no início do pipeline da sessão e disponibilizados em memória. Eles são recuperados e estruturados para compor as diretrizes operacionais e os contextos específicos do agente.

**Como os dados são usados no prompt?**
Os dados são divididos em dois níveis:

* **System Prompt:** Recebe regras gerais, metodologias de análise (ex: margem de segurança, três pilares da prosperidade) e parâmetros rígidos de conformidade/segurança.
* **Contexto Dinâmico (User Prompt / Context Ingestion):** Injeta apenas as variáveis específicas do cliente atual (ex: perfil, renda, metas) e a fatia relevante dos produtos de investimento/regras de mercado no momento da interação, garantindo precisão sem sobrecarregar a janela de contexto.

---

**Exemplo de Contexto Montado**

```
Dados do Cliente:
- Nome: João Silva[cite: 5]
- Idade: 32 anos | Profissão: Analista de Sistemas[cite: 5]
- Renda Mensal: R$ 5.000,00 | Patrimônio Total: R$ 15.000,00[cite: 5]
- Perfil de Investidor: Moderado[cite: 5]
- Objetivo Principal: Construir reserva de emergência[cite: 5]
- Reserva de Emergência Atual: R$ 10.000,00 (Meta: R$ 15.000,00 até 2026-06)[cite: 5]

Diretrizes de Investimento do Contexto:
- Regra de Liquidez Diária: Tesouro Selic e CDB Liquidez Diária (Rendimento de 100% a 102% do CDI / Selic)[cite: 3, 6].
- Regra do Perfil Moderado: Fundos Multimercado e LCI/LCA com foco em diversificação para as metas de médio/longo prazo[cite: 6].

Conceitos Relevantes da Base:
- Equação da Independência Financeira: Rendimento mensal dos investimentos >= Gastos totais mensais (Thiago Nigro)[cite: 7].
- Margem de Segurança: Foco na preservação do capital e mitigação de riscos emocionais do mercado (Benjamin Graham)[cite: 4].

```
...
```
