from knowledge_base import CHUNKS

def get_chunk(chunk_id: str) -> str:
    for c in CHUNKS:
        if c["id"] == chunk_id:
            return c["text"]
    return ""


GOLDEN_DATASET = [
    {
        "id": "q1",
        "input": "O que é um Teste de Aceitação e qual é seu objetivo principal?",
        "expected_output": (
            "Um Teste de Aceitação é aquele que verifica se o sistema atende aos critérios "
            "de aceitação de um requisito do ponto de vista do usuário ou negócio, de forma "
            "observável externamente. Deve ser a última ação de teste antes da implantação. "
            "O objetivo principal é a satisfação do cliente."
        ),
        "retrieval_context": [
            get_chunk("acceptance_definition"),
            get_chunk("acceptance_characteristics"),
        ],
    },
    {
        "id": "q2",
        "input": "Qual a diferença entre Teste de Unidade e Teste de Aceitação?",
        "expected_output": (
            "Testes de Unidade ajudam a escrever o código certo (verificam se o código "
            "está correto tecnicamente). Testes de Aceitação ajudam a escrever o código "
            "certo do ponto de vista do negócio (verificam se o sistema faz o que foi "
            "combinado com o cliente). Testes de unidade não garantem valor de negócio."
        ),
        "retrieval_context": [
            get_chunk("acceptance_vs_unit"),
            get_chunk("acceptance_definition"),
        ],
    },
    {
        "id": "q3",
        "input": "O que são critérios de aceitação e por que são importantes?",
        "expected_output": (
            "Critérios de aceitação são condições claras e verificáveis que definem quando "
            "uma funcionalidade está correta. São independentes de UI ou tecnologia. "
            "São importantes porque uma história de usuário sem critérios de aceitação "
            "não está pronta para desenvolvimento, e critérios não verificáveis não servem "
            "para teste."
        ),
        "retrieval_context": [
            get_chunk("acceptance_criteria"),
            get_chunk("acceptance_definition"),
        ],
    },
    {
        "id": "q4",
        "input": "O que é Gherkin e quais são suas palavras-chave principais?",
        "expected_output": (
            "Gherkin é a linguagem utilizada para especificar testes de aceitação em um "
            "formato legível por humanos e interpretável por máquinas. Suas palavras-chave "
            "são: Feature (descreve a funcionalidade), Scenario (caso específico), "
            "Given (contexto inicial/pré-condições), When (ação ou evento), "
            "Then (resultado esperado/comportamento observável)."
        ),
        "retrieval_context": [
            get_chunk("gherkin"),
            get_chunk("bdd"),
        ],
    },
    {
        "id": "q5",
        "input": "O que é BDD e qual é sua relação com testes de aceitação?",
        "expected_output": (
            "BDD (Behavior-Driven Development) é uma prática para descobrir, discutir e "
            "validar comportamentos esperados do sistema. Conecta requisitos de negócio e "
            "implementação técnica. Não é apenas sobre testes, é sobre construir "
            "entendimento compartilhado entre dev, QA e negócio. O Cucumber é a ferramenta "
            "que executa testes escritos em Gherkin, fazendo a ponte entre negócio e código."
        ),
        "retrieval_context": [
            get_chunk("bdd"),
            get_chunk("gherkin"),
        ],
    },
    {
        "id": "q6",
        "input": "O que é Teste de Integração e quais são suas estratégias?",
        "expected_output": (
            "Teste de Integração verifica se componentes que funcionam isoladamente também "
            "funcionam corretamente quando integrados, respeitando contratos, protocolos, "
            "fluxos de dados e efeitos colaterais. As estratégias são: Big-Bang (tudo de uma vez, "
            "sem isolamento de faltas), Top-Down (inicia na raiz com stubs, bom isolamento "
            "de faltas) e Bottom-Up (inicia nas folhas com drivers, condições mais simples)."
        ),
        "retrieval_context": [
            get_chunk("integration_definition"),
            get_chunk("integration_strategies"),
        ],
    },
    {
        "id": "q7",
        "input": "Como o Modelo V relaciona fases de desenvolvimento e fases de teste?",
        "expected_output": (
            "O Modelo V relaciona cada fase de desenvolvimento com sua fase de teste correspondente: "
            "Especificação de Requisitos corresponde ao Teste de Aceitação; "
            "Projeto de Alto Nível corresponde ao Teste de Sistema; "
            "Projeto Detalhado corresponde ao Teste de Integração; "
            "Codificação corresponde ao Teste de Unidade. "
            "Cada fase de desenvolvimento planeja antecipadamente sua fase de teste."
        ),
        "retrieval_context": [
            get_chunk("model_v"),
            get_chunk("integration_definition"),
        ],
    },
]