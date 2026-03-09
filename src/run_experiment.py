import os
import json
from dotenv import load_dotenv
from openai import OpenAI

import deepeval
from deepeval import evaluate
from deepeval.test_case import LLMTestCase
from deepeval.metrics import (
    AnswerRelevancyMetric,
    FaithfulnessMetric,
    HallucinationMetric,
    ContextualRecallMetric,
    ContextualPrecisionMetric,
)

from dataset import GOLDEN_DATASET
from prompts import PROMPT_1_CONFIG, PROMPT_2_CONFIG, PROMPT_3_CONFIG, PROMPT_4_CONFIG
from knowledge_base import retrieve_context

load_dotenv()

client = OpenAI(api_key=os.environ["OPENAI_API_KEY"])
MODEL = "gpt-4o-mini"  # troque para "gpt-4o" se quiser resultados mais robustos

CONFIDENT_API_KEY = os.environ.get("CONFIDENT_AI_API_KEY")
if CONFIDENT_API_KEY:
    deepeval.login_with_confident_api_key(CONFIDENT_API_KEY)


def get_metrics():
    return [
        AnswerRelevancyMetric(threshold=0.7, model="gpt-4o-mini", verbose_mode=False),
        FaithfulnessMetric(threshold=0.7, model="gpt-4o-mini", verbose_mode=False),
        HallucinationMetric(threshold=0.5, model="gpt-4o-mini", verbose_mode=False),
        ContextualRecallMetric(threshold=0.7, model="gpt-4o-mini", verbose_mode=False),
        ContextualPrecisionMetric(threshold=0.7, model="gpt-4o-mini", verbose_mode=False),
    ]

def generate_answer(prompt_config: dict, question: str, context_chunks: list[str]) -> str:
    context_text = "\n\n---\n\n".join(context_chunks)

    user_message = prompt_config["template"].format(
        context=context_text,
        question=question,
    )

    messages = []
    if prompt_config.get("system"):
        messages.append({"role": "system", "content": prompt_config["system"]})
    messages.append({"role": "user", "content": user_message})

    response = client.chat.completions.create(
        model=MODEL,
        messages=messages,
        temperature=prompt_config["temperature"],
        max_tokens=512,
    )

    return response.choices[0].message.content.strip()

def get_optimized_prompt() -> dict:
    optimized_file = "optimized_prompt.json"


    with open(optimized_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    optimized = data["optimized_prompt"]
    PROMPT_4_CONFIG["system"] = optimized
    PROMPT_4_CONFIG["template"] = "{context}\n\nQuestion: {question}\n\nAnswer:"
    PROMPT_4_CONFIG["temperature"] = data.get("temperature", 0.3)

    return PROMPT_4_CONFIG

def run_experiment(prompt_config: dict, experiment_name: str) -> list[LLMTestCase]:
    print(f"\n{'='*60}")
    print(f"🧪 Experimento: {experiment_name}")
    print(f"   {prompt_config['description']}")
    print(f"   Temperatura: {prompt_config['temperature']}")
    print(f"{'='*60}")

    test_cases = []

    for entry in GOLDEN_DATASET:
        print(f"  → Gerando resposta para: {entry['input'][:60]}...")

        answer = generate_answer(
            prompt_config=prompt_config,
            question=entry["input"],
            context_chunks=entry["retrieval_context"],
        )

        test_case = LLMTestCase(
            input=entry["input"],
            actual_output=answer,
            expected_output=entry["expected_output"],
            retrieval_context=entry["retrieval_context"],
            context=entry["retrieval_context"],
        )
        test_cases.append(test_case)

    return test_cases

def evaluate_experiment(test_cases: list[LLMTestCase], experiment_name: str) -> dict:
    print(f"\n📊 Avaliando: {experiment_name}...")

    metrics = get_metrics()
    results = evaluate(
        test_cases=test_cases,
        metrics=metrics,
        run_async=False,
        print_results=False,
    )

    # Agrega scores por métrica
    metric_scores = {}
    for test_result in results.test_results:
        for metric_data in test_result.metrics_data:
            name = metric_data.name
            score = metric_data.score or 0.0
            if name not in metric_scores:
                metric_scores[name] = []
            metric_scores[name].append(score)

    avg_scores = {
        name: round(sum(scores) / len(scores), 3)
        for name, scores in metric_scores.items()
    }

    return avg_scores


def print_report(all_results: dict):
    print(f"\n{'='*70}")
    print("📈 RELATÓRIO FINAL — Comparação entre os 4 Prompts")
    print(f"{'='*70}")

    metric_names = list(next(iter(all_results.values())).keys())
    col_width = 28

    # Cabeçalho
    header = f"{'Métrica':<{col_width}}"
    for exp_name in all_results:
        short = exp_name.split("—")[0].strip()
        header += f"{short:>14}"
    print(header)
    print("-" * (col_width + 14 * len(all_results)))

    # Linhas
    for metric in metric_names:
        row = f"{metric:<{col_width}}"
        for exp_name, scores in all_results.items():
            val = scores.get(metric, 0.0)
            emoji = "✅" if val >= 0.7 else ("⚠️ " if val >= 0.5 else "❌")
            row += f"{emoji} {val:>8.3f}  "
        print(row)

    print(f"\n{'='*70}")
    print("Legenda: ✅ ≥ 0.7 (bom)  |  ⚠️  0.5–0.7 (atenção)  |  ❌ < 0.5 (ruim)")
    print(f"{'='*70}")

    # Salva JSON para consulta
    with open("results.json", "w", encoding="utf-8") as f:
        json.dump(all_results, f, indent=2, ensure_ascii=False)
    print("\n💾 Resultados salvos em results.json")


# ------------------------------------------------------------------------------
# Main
# ------------------------------------------------------------------------------
def main():
    print("\n🚀 DeepEval Demo — V&V UFCG")
    print("   Comparando 4 estratégias de prompt em RAG sobre material de V&V\n")

    get_optimized_prompt()

    experiments = [
        (PROMPT_1_CONFIG, "Prompt 1 — Simples"),
        (PROMPT_2_CONFIG, "Prompt 2 — Alta Temperatura"),
        (PROMPT_3_CONFIG, "Prompt 3 — Padrão da Indústria"),
        (PROMPT_4_CONFIG, "Prompt 4 — Otimizado pelo DeepEval"),
    ]

    all_results = {}

    for prompt_config, exp_name in experiments:
        test_cases = run_experiment(prompt_config, exp_name)
        scores = evaluate_experiment(test_cases, exp_name)
        all_results[exp_name] = scores

        print(f"\n  Scores médios — {exp_name}:")
        for metric, score in scores.items():
            print(f"    {metric}: {score:.3f}")

    print_report(all_results)

    if CONFIDENT_API_KEY:
        print("\n🌐 Resultados enviados para o dashboard do Confident AI!")
        print("   Acesse: https://app.confident-ai.com")


if __name__ == "__main__":
    main()