import os
import json
from deepeval.prompt_optimizer import PromptOptimizer

from prompts import PROMPT_1_CONFIG
from dataset import GOLDEN_DATASET
from knowledge_base import retrieve_context

OUTPUT_FILE = "optimized_prompt.json"


def build_examples() -> list[dict]:
    examples = []
    for entry in GOLDEN_DATASET:
        ctx = "\n\n".join(entry["retrieval_context"])
        examples.append({
            "input": PROMPT_1_CONFIG["template"].format(
                context=ctx,
                question=entry["input"],
            ),
            "expected_output": entry["expected_output"],
        })
    return examples


def main():
    print("\n DeepEval Prompt Optimizer")
    print("   Ponto de partida: Prompt 1 (Simples/Naive)")
    print("   Dataset: 7 perguntas de V&V\n")

    original_prompt = PROMPT_1_CONFIG["system"] + "\n\n" + PROMPT_1_CONFIG["template"]
    examples = build_examples()

    print(f"  Prompt original:\n{'─'*50}")
    print(original_prompt)
    print(f"{'─'*50}\n")

    print("  Otimizando... (pode levar alguns segundos)\n")

    try:
        optimizer = PromptOptimizer(
            model="gpt-4o-mini",
            original_prompt=original_prompt,
            examples=examples,
        )
        optimized = optimizer.optimize()

        result = {
            "original_prompt": original_prompt,
            "optimized_prompt": optimized,
            "temperature": 0.3,
        }

        with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)

        print(f"  Prompt otimizado salvo em: {OUTPUT_FILE}\n")
        print(f"  Prompt otimizado:\n{'─'*50}")
        print(optimized)
        print(f"{'─'*50}\n")
        
    except (ImportError, Exception) as e:
        print(f" Erro ao otimizar: {e}")
        print("  Verifique se o DeepEval está atualizado: pip install --upgrade deepeval\n")


if __name__ == "__main__":
    main()