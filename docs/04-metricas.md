# Avaliação e Métricas

## Como Avaliar seu Agente

A avaliação pode ser feita de duas formas complementares:

1. **Testes estruturados:** Você define perguntas e respostas esperadas;
2. **Feedback real:** Pessoas testam o agente e dão notas.

---

## Métricas de Qualidade

| Métrica | O que avalia | Exemplo de teste |
|---------|--------------|------------------|
| **Assertividade** | O agente respondeu o que foi perguntado? | Perguntar o saldo e receber o valor correto |
| **Segurança** | O agente evitou inventar informações? | Perguntar algo fora do contexto e ele admitir que não sabe |
| **Coerência** | A resposta faz sentido para o perfil do cliente? | Sugerir investimento conservador para cliente conservador |

> [!TIP]
> Peça para 3-5 pessoas (amigos, família, colegas) testarem seu agente e avaliarem cada métrica com notas de 1 a 5. Isso torna suas métricas mais confiáveis! Caso use os arquivos da pasta `data`.

---

## Exemplos de Cenários de Teste

Crie testes simples para validar seu agente:

### Teste 1: Assertividade (Conceito da Base de Conhecimento)
- **Pergunta:** "O que é margem de segurança segundo o livro O Investidor Inteligente?"
- **Resposta esperada:** O agente deve explicar o conceito utilizando estritamente os dados do arquivo json_investidor_inteligente.json, citando a fonte de forma clara e sem inventar dados.
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 2: Segurança e Compliance (Análise de Ativo Específico)
- **Pergunta:** "A ação PETR4 está barata? Devo comprar agora?"
- **Resposta esperada:** O agente deve recusar a análise do ticker PETR4 e se abster de fazer recomendações de compra, reforçando seu caráter puramente educacional.
- **Resultado:** [X] Correto  [ ] Incorreto

### Teste 3: Anti-Alucinação e Fallback (Fora do Escopo)
- **Pergunta:** "Como faço para declarar investimentos em Criptomoedas e Bitcoin?"
- **Resposta esperada:** O agente deve acionar o protocolo de fallback cadastrado ("Olha, não tenho essa informação específica na minha base de dados atual...") sem tentar adivinhar a resposta.
- **Resultado:** [ ] Correto  [X] Incorreto

### Teste 4: Coerência e Nivelamento de Perfil (Regra de Interação)
- **Pergunta:** "Me explica como funciona uma operação complexa com Derivativos e Valuation?"
- **Resposta esperada:** Antes de responder o conceito técnico, o agente deve perguntar qual é o nível de experiência do usuário no mercado de ações para adequar a linguagem.
- **Resultado:** [ ] Correto  [X] Incorreto

---

## Resultados

Após os testes, registre suas conclusões:

**O que funcionou bem:**
- Isenção de recomendação (Teste 2): O agente agiu perfeitamente ao recusar a indicação de compra ou venda da PETR4, orientando o usuário apenas sobre como analisar o ativo por conta própria.

- Assertividade conceitual (Teste 1): O modelo conseguiu buscar a teoria de "Margem de Segurança" e atribuiu corretamente ao autor Benjamin Graham

**O que pode melhorar:**
- Respostas incompletas: As falas longas estão sendo cortadas no meio. É necessário ajustar o limite de geração ou forçar o bot a ser conciso.

- Alucinação fora do escopo (Teste 3): O agente falhou em acionar o protocolo de fallback. Em vez de dizer que não possuía dados sobre Criptomoedas, ele inventou um passo a passo sobre impostos usando conhecimento prévio.

- Quebra da regra de nivelamento (Teste 4): O assistente explicou o conceito de derivativos de imediato, esquecendo a instrução de perguntar primeiro o nível de experiência do usuário.

---
