import os
import pytest
from dotenv import load_dotenv
from deepeval import assert_test
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    HallucinationMetric,
    ContextualRecallMetric,
    ContextualPrecisionMetric,
)
from deepeval.models import GeminiModel

load_dotenv()

gemini_judge = GeminiModel(
    model="gemini-2.5-flash",
    api_key=os.environ["GOOGLE_API_KEY"],
    temperature=0
)

metricas_totais = [
    AnswerRelevancyMetric(threshold=0.7, model=gemini_judge, verbose_mode=False),
    FaithfulnessMetric(threshold=0.7, model=gemini_judge, verbose_mode=False),
    HallucinationMetric(threshold=0.5, model=gemini_judge, verbose_mode=False),
    ContextualRecallMetric(threshold=0.7, model=gemini_judge, verbose_mode=False),
    ContextualPrecisionMetric(threshold=0.7, model=gemini_judge, verbose_mode=False),
]

# =====================================================================
# DADOS BASE PARA A DEMONSTRAÇÃO
# =====================================================================
INPUT_USUARIO = "Quais são as orientações do SUS para o tratamento da Dengue e quais os medicamentos proibidos?"

OUTPUT_ESPERADO = (
    "As orientações do SUS para a Dengue indicam muita hidratação e repouso. "
    "É expressamente proibido o uso de medicamentos como AAS e Ibuprofeno, "
    "devido ao alto risco de hemorragias."
)

# =====================================================================
# CASO 1: O RAG PERFEITO ✅ (O seu projeto bem feito)
# =====================================================================
def test_rag_perfeito():
    contexto_excelente = [
        "Diretriz SUS (Dengue): A base do tratamento para a dengue é a hidratação intensiva e o repouso. Não há medicamento específico contra o vírus.",
        "Contraindicações (Dengue): Nunca utilize medicamentos derivados do ácido acetilsalicílico (AAS) ou anti-inflamatórios como o Ibuprofeno, pois aumentam o risco de hemorragias."
    ]
    
    resposta_ia_perfeita = (
        "De acordo com o SUS, o tratamento para a dengue baseia-se em repouso e muita hidratação. "
        "Não deve utilizar medicamentos como AAS ou Ibuprofeno, pois existe o risco de causarem hemorragias."
    )
    
    test_case = LLMTestCase(
        input=INPUT_USUARIO,
        actual_output=resposta_ia_perfeita,
        expected_output=OUTPUT_ESPERADO,
        retrieval_context=contexto_excelente,
        context=contexto_excelente
    )
    
    print("\n[A TESTAR] Cenário 1: O RAG Perfeito (Tudo Verde)...")
    assert_test(test_case, metricas_totais)

def test_rag_desastroso():
    contexto_pessimo = [
        "Campanha de Vacinação: O SUS informa que a vacina da gripe está disponível em todos os postos.", # Irrelevante!
        "Diretriz SUS (Dengue): O paciente com dengue deve manter-se hidratado." # Incompleto (falta a contraindicação)
    ]

    resposta_ia_alucinada = (
        "A vacina da gripe está disponível nos postos do SUS. Para a dengue, a recomendação "
        "é beber muita água. Além disso, recomendo que tome um chá de amora com paracetamol "
        "de 8 em 8 horas para passar a febre mais rápido."
    )
    
    test_case = LLMTestCase(
        input=INPUT_USUARIO,
        actual_output=resposta_ia_alucinada,
        expected_output=OUTPUT_ESPERADO,
        retrieval_context=contexto_pessimo,
        context=contexto_pessimo
    )
    
    print("\n[A TESTAR] Cenário 2: O RAG Desastroso (Tudo Vermelho)...")
    assert_test(test_case, metricas_totais)