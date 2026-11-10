import streamlit as st
from groq import Groq
import re

# Configuração da página e Estilo Imersivo ASOIAF (Cores escuras, dourado, vermelho dragão e visual medieval)
st.set_page_config(page_title="ASOIAF - White List Evaluation Center", page_icon="⚔️", layout="wide")

st.markdown("""
    <style>
    @import url('https://googleapis.com');
    
    /* Fundo e Container Principal */
    .stApp {
        background-color: #111111;
        color: #e0e0e0;
        font-family: 'Montserrat', sans-serif;
    }
    
    /* Títulos Estilo Medieval */
    h1, h2, h3 {
        font-family: 'Cinzel', serif;
        color: #ffd700;
        text-align: center;
        text-shadow: 2px 2px 4px #000000;
    }
    
    /* Bordas e Caixas de Pergunta */
    .question-box {
        background-color: #1a1a1a;
        border: 2px solid #8b0000;
        border-radius: 8px;
        padding: 20px;
        margin-bottom: 25px;
        box-shadow: 5px 5px 15px rgba(0,0,0,0.5);
    }
    
    .question-title {
        font-family: 'MedievalSharp', cursive;
        color: #ff4500;
        font-size: 1.2rem;
        border-bottom: 1px solid #333;
        padding-bottom: 8px;
        margin-bottom: 12px;
    }
    
    /* Status de Notas */
    .rating-badge {
        font-weight: bold;
        padding: 4px 8px;
        border-radius: 4px;
        text-transform: uppercase;
    }
    
    /* Botão de Envio */
    .stButton>button {
        background-color: #8b0000 !important;
        color: #ffffff !important;
        font-family: 'Cinzel', serif !important;
        font-size: 1.2rem !important;
        width: 100%;
        border: 1px solid #ffd700 !important;
        transition: 0.3s;
    }
    def:hover {
        background-color: #ff4500 !important;
        box-shadow: 0px 0px 15px #ffd700;
    }
    </style>
""", unsafe_allow_html=True)

# Inicializa o cliente Groq - Insira sua chave gratuita aqui ou configure nos Secrets da Nuvem
# Para testar localmente, você pode colar sua chave direto entre as aspas
GROQ_API_KEY = st.sidebar.text_input("Insira sua Groq API Key:", type="password")

st.title("⚔️ ASOIAF – WHITE LIST EVALUATION CENTER ⚔️")
st.write("<p style='text-align:center; font-style:italic; color:#aaa;'>Mecanismo de Julgamento Automatizado para a Patrulha da Noite e Grandes Casas</p>", unsafe_allow_html=True)

# Definição das Regras do Sistema para injetar na IA
SYSTEM_PROMPT = """You are the Grand Maester Assistant responsible for evaluating candidate application forms (White Lists) for an ASOIAF (A Song of Ice and Fire) RP Server.
Your role is to strictly judge the answers submitted by candidates based on the 10 Evaluation Rules provided below. 

You must evaluate each of the 11 Predefined Questions individually.
For each question, output the candidate's original answer, assign a rating exactly from this list: [Perfect, Good, OK, Satisfactory, Insufficient, Poor, Terrible], and explain your assessment based on the rules.

At the very end, give a Final Decision: APPROVED or REJECTED.
If REJECTED, list the exact rules violated and give a solid justification. Do not use any evaluator names.

CRITICAL RULES TO ENFORCE:
1. "I don't know" answers: Reject immediately.
2. Religions and Continents: Must describe characteristics, beliefs, customs. Vague answers like "The Faith of the Seven is dominant in the south" without context = Reject.
3. Minimum Required: Answers about religions and continents MUST include at least 3 religions and 3 continents. Less than 3 = Reject.
4. Quality: Answers too short, generic, or incomplete = Reject.
5. Tolerance: Allow slight typos if real effort and lore knowledge are visible. Do not tolerate lack of effort or factual contradictions.
6. AI Content: Strictly prohibited. If answers look AI-generated, note it and Reject.
7. Lore Consistency: Incompatible/invented facts not allowed.
8. Interpretation: Must answer exactly what is requested.
9. Length doesn't mean quality. Focus on substance and effort.

Predefined Questions to map against the input:
Q1: What is your Roblox username?
Q2: Explain what permadeath means in your own words.
Q3: How involved do you intend to be with the lore?
Q4: What is the capital of the Seven Kingdoms?
Q5: How does the feudal system work in Westeros?
Q6: What is the purpose of the Night's Watch?
Q7: What is your favorite House in ASOIAF, and why?
Q8: What is your favorite era of ASOIAF, and why?
Q9: Briefly describe the main religions of ASOIAF.
Q10: Name and briefly describe the continents.
Q11: What would you bring to CGF?

Provide the response in clear Markdown format. Structure it so each question is clearly separated so the app can render it elegantly."""

# TELA 1: Envio do Formulário
if "evaluation_results" not in st.session_state:
    st.subheader("📜 Submissão do Formulário da White List")
    st.write("Cole abaixo o formulário completo preenchido pelo candidato (contendo as perguntas e respostas ou apenas o bloco de texto corrido).")
    
    raw_form = st.text_area("Formulário do Candidato:", height=400, placeholder="Exemplo:\n1. MeuNickRoblox\n2. Permadeath significa que se o personagem morrer, ele morre para sempre...\n3. Quero participar de eventos...")
    
    if st.button("Iniciar Julgamento da IA"):
        if not GROQ_API_KEY:
            st.error("Por favor, insira sua Groq API Key na barra lateral esquerda para continuar.")
        elif not raw_form.strip():
            st.error("O formulário não pode estar vazio.")
        else:
            with st.spinner("O Grande Master está analisando os pergaminhos..."):
                try:
                    client = Groq(api_key=GROQ_API_KEY)
                    # Usando o Llama 3.3 70B Versatile (Melhor modelo gratuito da Groq para raciocínio complexo)
                    completion = client.chat.completions.create(
                        model="llama-3.3-70b-versatile",
                        messages=[
                            {"role": "system", "content": SYSTEM_PROMPT},
                            {"role": "user", "content": f"Please evaluate this application form text:\n\n{raw_form}"}
                        ],
                        temperature=0.2, # Baixa temperatura garante consistência jurídica nas regras
                    )
                    st.session_state.evaluation_results = completion.choices.message.content
                    st.rerun()
                except Exception as e:
                    st.error(f"Erro ao consultar a IA: {e}")

# TELA 2: Painel de Avaliação Imersivo
else:
    st.subheader("🦅 Veredito do Grande Maester")
    
    # Exibe o resultado bruto formatado elegantemente
    st.markdown(st.session_state.evaluation_results)
    
    if st.button("🧾 Avaliar Nova White List"):
        del st.session_state.evaluation_results
        st.rerun()
