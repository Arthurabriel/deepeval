import os
import json
import pytest
from dotenv import load_dotenv
from google import genai
from google.genai import types

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

from dataset import GOLDEN_DATASET
from prompts import PROMPT_1_CONFIG, PROMPT_2_CONFIG, PROMPT_3_CONFIG, PROMPT_4_CONFIG

# ------------------------------------------------------------------------------
# SETUP & CONFIGURAÇÃO
# ------------------------------------------------------------------------------
load_dotenv()

GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY não encontrada no arquivo .env")

client = genai.Client(api_key=GOOGLE_API_KEY)
MODEL_NAME = "gemini-2.5-flash"

# Instancia o Juiz
gemini_judge = GeminiModel(
    model=MODEL_NAME,
    api_key=GOOGLE_API_KEY,
    temperature=0
)

quality_metrics = [
    AnswerRelevancyMetric(threshold=0.7, model=gemini_judge, verbose_mode=False),
    FaithfulnessMetric(threshold=0.7, model=gemini_judge, verbose_mode=False),
    HallucinationMetric(threshold=0.5, model=gemini_judge, verbose_mode=False),
    ContextualRecallMetric(threshold=0.7, model=gemini_judge, verbose_mode=False),
    ContextualPrecisionMetric(threshold=0.7, model=gemini_judge, verbose_mode=False),
]

# ------------------------------------------------------------------------------
# FUNÇÕES DE APOIO
# ------------------------------------------------------------------------------

def get_optimized_prompt() -> dict:
    optimized_file = "results/optimized_prompt.json"
    if not os.path.exists(optimized_file):
        return PROMPT_4_CONFIG

    with open(optimized_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    PROMPT_4_CONFIG["system"] = data["optimized_prompt"]
    PROMPT_4_CONFIG["template"] = "{context}\n\nQuestion: {question}\n\nAnswer:"
    PROMPT_4_CONFIG["temperature"] = data.get("temperature", 0.3)
    return PROMPT_4_CONFIG

PROMPT_4_OTIMIZADO = get_optimized_prompt()

def generate_answer(prompt_config: dict, question: str, context_chunks: list[str]) -> str:
    context_text = "\n\n---\n\n".join(context_chunks)
    user_message = prompt_config["template"].format(context=context_text, question=question)

    config_kwargs = {
        "temperature": prompt_config.get("temperature", 0.2),
        "max_output_tokens": 512,
    }

    if prompt_config.get("system"):
        config_kwargs["system_instruction"] = prompt_config["system"]

    response = client.models.generate_content(
        model=MODEL_NAME,
        contents=user_message,
        config=types.GenerateContentConfig(**config_kwargs),
    )
    return response.text.strip()

@pytest.mark.parametrize("case_data", GOLDEN_DATASET)
def test_prompt_1_simples(case_data):
    actual_output = generate_answer(PROMPT_1_CONFIG, case_data["input"], case_data["retrieval_context"])
    
    test_case = LLMTestCase(
        input=case_data["input"],
        actual_output=actual_output,
        expected_output=case_data["expected_output"],
        retrieval_context=case_data["retrieval_context"],
        context=case_data["retrieval_context"]
    )
    assert_test(test_case, quality_metrics)


@pytest.mark.parametrize("case_data", GOLDEN_DATASET)
def test_prompt_2_alta_temperatura(case_data):
    actual_output = generate_answer(PROMPT_2_CONFIG, case_data["input"], case_data["retrieval_context"])
    
    test_case = LLMTestCase(
        input=case_data["input"],
        actual_output=actual_output,
        expected_output=case_data["expected_output"],
        retrieval_context=case_data["retrieval_context"],
        context=case_data["retrieval_context"]
    )
    assert_test(test_case, quality_metrics)


@pytest.mark.parametrize("case_data", GOLDEN_DATASET)
def test_prompt_3_padrao_industria(case_data):
    actual_output = generate_answer(PROMPT_3_CONFIG, case_data["input"], case_data["retrieval_context"])
    
    test_case = LLMTestCase(
        input=case_data["input"],
        actual_output=actual_output,
        expected_output=case_data["expected_output"],
        retrieval_context=case_data["retrieval_context"],
        context=case_data["retrieval_context"]
    )
    assert_test(test_case, quality_metrics)


@pytest.mark.parametrize("case_data", GOLDEN_DATASET)
def test_prompt_4_otimizado(case_data):
    actual_output = generate_answer(PROMPT_4_OTIMIZADO, case_data["input"], case_data["retrieval_context"])
    
    test_case = LLMTestCase(
        input=case_data["input"],
        actual_output=actual_output,
        expected_output=case_data["expected_output"],
        retrieval_context=case_data["retrieval_context"],
        context=case_data["retrieval_context"]
    )
    assert_test(test_case, quality_metrics)