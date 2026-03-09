PROMPT_1_SYSTEM = "You are a helpful assistant. Answer the question using the context provided."

PROMPT_1_TEMPLATE = """Context:
{context}

Question: {question}

Answer:"""

PROMPT_1_CONFIG = {
    "name": "Prompt 1 — Simples",
    "system": PROMPT_1_SYSTEM,
    "template": PROMPT_1_TEMPLATE,
    "description": "Prompt minimalista, sem restrições sobre uso do contexto.",
}

PROMPT_2_SYSTEM = "You are a helpful assistant. Answer the question using the context provided."

PROMPT_2_TEMPLATE = """Context:
{context}

Question: {question}

Answer:"""

PROMPT_2_CONFIG = {
    "name": "Prompt 2 — Alta Temperatura (alucinação)",
    "temperature": 2.0,
    "system": PROMPT_2_SYSTEM,
    "template": PROMPT_2_TEMPLATE,
    "description": "Mesmo prompt simples com temperatura 2.0 para induzir alucinações.",
}

PROMPT_3_SYSTEM = (
    "You are a precise technical assistant specialized in answering questions "
    "about software testing and verification & validation (V&V) concepts. "
    "Your role is to provide accurate, grounded answers based solely on the "
    "provided context."
)

PROMPT_3_TEMPLATE = """Use ONLY the information provided in the context below to answer the question.
If the answer is not present in the context, respond with:
"I don't have enough information to answer this question based on the provided material."

Do NOT invent information, infer beyond what is stated, or use external knowledge.
Be concise, factual, and use the domain language from the context.

Context:
{context}

Question: {question}

Answer (based strictly on the context above):"""

PROMPT_3_CONFIG = {
    "name": "Prompt 3 — Padrão da Indústria",
    "temperature": 0.2,
    "system": PROMPT_3_SYSTEM,
    "template": PROMPT_3_TEMPLATE,
    "description": "Prompt com boas práticas: restrição ao contexto, instrução de fallback, temperatura baixa.",
}

PROMPT_4_CONFIG = {
    "name": "Prompt 4 — Otimizado pelo DeepEval",
    "temperature": 0.3,
    "system": None,   # será preenchido pelo otimizador
    "template": None, # será preenchido pelo otimizador
    "description": "Prompt gerado automaticamente pelo otimizador do DeepEval a partir do Prompt 1.",
}


ALL_PROMPTS = [PROMPT_1_CONFIG, PROMPT_2_CONFIG, PROMPT_3_CONFIG, PROMPT_4_CONFIG]