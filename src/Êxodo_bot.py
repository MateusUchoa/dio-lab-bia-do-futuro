import json
import os
import re
 
import ollama
import streamlit as st
 
# ================= CONFIGURAÇÕES DO MODELO ====================
MODELO = "qwen2.5-coder:14b"
LIMITE_HISTORICO = 10
 
 
# =============== CARREGAMENTO DOS DADOS =================
def carregar_json(caminho):
    if not os.path.exists(caminho):
        return {}
 
    try:
        with open(caminho, "r", encoding="utf-8") as arquivo:
            return json.load(arquivo)
    except (json.JSONDecodeError, OSError) as erro:
        st.warning(f"Não foi possível carregar {caminho}: {erro}")
        return {}
 
 
CVM = carregar_json("CVM_bolsa.json")
glossario = carregar_json("glossario_b3_base.json")
jovens_bolsa = carregar_json("jovens_na_bolsa.json")
investidor_inteligente = carregar_json("json_investidor_inteligente.json")
perfil = carregar_json("perfil_investidor.json")
produtos = carregar_json("produtos_financeiros.json")
mil_milhao = carregar_json("json_mil_ao_milhao.json")
 
# =============== PROMPT DE SISTEMA COM TRAVAS DURAS =================
SYSTEM_PROMPT_BASE = """
Você é o Êxodo Bot, um mentor educacional financeiro para iniciantes.
 
OBJETIVO:
Ensinar conceitos de investimentos de maneira simples, objetiva, responsável e educativa.
 
ESTILO:
- Responda em português do Brasil.
- Seja direto, acolhedor e didático.
- Faça no máximo uma pergunta por resposta.
- Prefira respostas curtas com até 5 tópicos.
 
REGRAS INEGOCIÁVEIS DE SEGURANÇA E COMPLIANCE:
1. SEJA CONCISO: Responda em no máximo 2 parágrafos curtos para evitar cortes no streaming.
2. TRAVA DE CRIPTO E FORA DO ESCOPO: Se o usuário perguntar sobre Criptomoedas, Bitcoin, declaração de imposto de renda sobre cripto ou assuntos fora do mercado financeiro tradicional, RECUSE responder. Diga: "Olha, não tenho essa informação na minha base de dados atual e, como lidamos com o seu dinheiro, prefiro não inventar respostas."
3. TRAVA DE NIVELAMENTO: Se perguntarem sobre derivativos, opções, swap ou valuation complexo, NÃO EXPLIQUE O CONCEITO de imediato. Responda APENAS: "Antes de mergulharmos nisso, qual é o seu nível de experiência com a Bolsa de Valores?"
4. SEM RECOMENDAÇÕES OU AVALIAÇÃO DE ATIVOS: Se mencionarem um ticker específico (ex: PETR4, MXRF11, VALE3) perguntando se é bom, ruim, se deve comprar ou vender, recuse a análise direta. Forneça apenas conceitos teóricos gerais de análise se disponíveis na base.
5. RESTRIÇÃO DE BASE (ANTI-ALUCINAÇÃO): Use estritamente as informações fornecidas no contexto. Se uma informação financeira não constar na base enviada, acione o protocolo de fallback: "Não encontrei essa informação na minha base atual. Como o assunto envolve decisões financeiras, prefiro não inventar uma resposta."
"""
 
MENSAGEM_INICIAL = """
Olá! Eu sou o **Êxodo Bot**, seu mentor educacional para os primeiros passos no mundo dos investimentos.
 
Meu objetivo é explicar o mercado financeiro de forma simples e responsável. Posso ajudar você a entender:
 
- Ações, fundos imobiliários, ETFs e renda fixa;
- Risco, retorno, liquidez e diversificação;
- Funcionamento da Bolsa de Valores;
- Perfil de investidor;
- Termos financeiros e cuidados antes de investir.
 
Não faço recomendações de compra ou venda e não prometo rentabilidade.
 
Para começarmos, **como você gostaria de ser chamado?**
"""
 
 
# =============== FUNÇÕES AUXILIARES =================
def extrair_nome(texto):
    padroes = [
        r"meu nome é\s+([A-Za-zÀ-ÿ]+)",
        r"me chamo\s+([A-Za-zÀ-ÿ]+)",
        r"pode me chamar de\s+([A-Za-zÀ-ÿ]+)",
    ]
 
    for padrao in padroes:
        resultado = re.search(padrao, texto, flags=re.IGNORECASE)
        if resultado:
            return resultado.group(1).strip().title()
 
    return None
 
 
def selecionar_contexto(pergunta):
    pergunta = pergunta.lower()
    partes = []
 
    if any(
        palavra in pergunta
        for palavra in ["cvm", "regulamentação", "regulação", "fraude", "regra"]
    ):
        partes.append(
            "[DIRETRIZES CVM]\n" + json.dumps(CVM, ensure_ascii=False)
        )
 
    if any(
        palavra in pergunta
        for palavra in [
            "significa",
            "o que é",
            "termo",
            "ação",
            "fii",
            "etf",
            "dividendo",
            "glossário",
        ]
    ):
        partes.append(
            "[GLOSSÁRIO B3]\n" + json.dumps(glossario, ensure_ascii=False)
        )
 
    if any(
        palavra in pergunta
        for palavra in [
            "produto",
            "renda fixa",
            "tesouro",
            "cdb",
            "fundo",
            "renda variável",
        ]
    ):
        partes.append(
            "[PRODUTOS FINANCEIROS]\n" + json.dumps(produtos, ensure_ascii=False)
        )
 
    if any(
        palavra in pergunta
        for palavra in [
            "margem",
            "segurança",
            "graham",
            "valor intrínseco",
            "investidor inteligente",
        ]
    ):
        partes.append(
            "[LIVRO O INVESTIDOR INTELIGENTE]\n"
            + json.dumps(investidor_inteligente, ensure_ascii=False)
        )
 
    if any(
        palavra in pergunta
        for palavra in [
            "milhão",
            "nigro",
            "gasto",
            "poupar",
            "rentabilidade",
            "do mil ao milhão",
        ]
    ):
        partes.append(
            "[LIVRO DO MIL AO MILHÃO]\n"
            + json.dumps(mil_milhao, ensure_ascii=False)
        )
 
    if not partes:
        return (
            "ALERTA AO SISTEMA: Nenhuma seção da base de conhecimento continha palavras-chave "
            "correspondentes a esta pergunta. Se a dúvida for sobre dados financeiros específicos "
            "ou temas fora do escopo, acione imediatamente o protocolo de fallback."
        )
 
    return "\n\n".join(partes)
 
 
def gerar_resposta_stream(historico_mensagens):
    ultima_pergunta = historico_mensagens[-1]["content"]
    contexto_base = selecionar_contexto(ultima_pergunta)
    nome_usuario = st.session_state.get("nome_usuario")
 
    contexto_sessao = f"""
INFORMAÇÕES DA SESSÃO
Nome informado pelo usuário: {nome_usuario or "Ainda não informado"}
 
CONTEÚDO FINANCEIRO SELECIONADO DA BASE
{contexto_base}
"""
 
    historico_recente = historico_mensagens[-LIMITE_HISTORICO:]
 
    mensagens_completas = [
        {"role": "system", "content": SYSTEM_PROMPT_BASE},
        {"role": "system", "content": contexto_sessao},
    ] + historico_recente
 
    stream = ollama.chat(
        model=MODELO,
        messages=mensagens_completas,
        stream=True,
        options={
            "temperature": 0.3,
            "top_p": 0.9,
            "num_predict": 350,
        },
    )
 
    for chunk in stream:
        conteudo = chunk.get("message", {}).get("content", "")
        if conteudo:
            yield conteudo
 
 
# ====================== INTERFACE STREAMLIT ==============================
st.title("Êxodo Bot")
st.write(
    "Educação financeira para seus primeiros passos no mercado de investimentos."
)
 
if "nome_usuario" not in st.session_state:
    st.session_state.nome_usuario = None
 
if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": MENSAGEM_INICIAL}
    ]
 
for mensagem in st.session_state.messages:
    with st.chat_message(mensagem["role"]):
        st.markdown(mensagem["content"])
 
if prompt := st.chat_input("Digite sua pergunta ao Êxodo Bot..."):
    nome_encontrado = extrair_nome(prompt)
    if nome_encontrado:
        st.session_state.nome_usuario = nome_encontrado
 
    st.session_state.messages.append({"role": "user", "content": prompt})
 
    with st.chat_message("user"):
        st.markdown(prompt)
 
    with st.chat_message("assistant"):
        resposta_completa = st.write_stream(
            gerar_resposta_stream(st.session_state.messages)
        )
 
    st.session_state.messages.append(
        {"role": "assistant", "content": resposta_completa}
    )
