CHUNKS = [
    {
        "id": "acceptance_definition",
        "text": (
            "Um Teste de Aceitação é um teste que verifica se o sistema atende "
            "aos critérios de aceitação de um requisito, do ponto de vista do usuário "
            "ou negócio, de forma observável externamente. "
            "Os testes de aceitação devem ser a última ação de teste antes da implantação "
            "do software. Comportamentos são definidos a partir das necessidades do cliente. "
            "O objetivo principal é a satisfação do cliente."
        ),
    },
    {
        "id": "acceptance_vs_unit",
        "text": (
            "Testes de Unidade ajudam a escrever o código certo. "
            "Testes de Aceitação ajudam a escrever o código certo do ponto de vista do negócio. "
            "Testes de unidade não garantem valor de negócio. "
            "A diferença principal: unidade verifica se o código está correto; "
            "aceitação verifica se o sistema faz o que foi combinado com o cliente."
        ),
    },
    {
        "id": "acceptance_characteristics",
        "text": (
            "Características essenciais dos Testes de Aceitação: "
            "foco em comportamento, não implementação; "
            "linguagem do domínio, não técnica; "
            "valida valor entregue, não cobertura de código; "
            "pode ou não ser automatizado. "
            "O que NÃO é teste de aceitação: teste de unidade grande, "
            "teste de interface por si só, teste técnico disfarçado de funcional."
        ),
    },
    {
        "id": "acceptance_criteria",
        "text": (
            "Critérios de Aceitação são condições claras e verificáveis que definem "
            "quando uma funcionalidade está correta. São independentes de UI ou tecnologia. "
            "'História sem critério de aceitação não está pronta para desenvolvimento.' "
            "'Se o critério não é verificável, ele não serve para teste.' "
            "Histórias de usuário sem critérios de aceitação geram ambiguidade entre "
            "dev, QA e cliente."
        ),
    },
    {
        "id": "gherkin",
        "text": (
            "Gherkin é a linguagem utilizada para especificar os testes de aceitação "
            "em um formato legível por humanos e interpretável por máquinas. "
            "Palavras-chave: Feature descreve a funcionalidade ou requisito de negócio; "
            "Scenario representa um caso específico; "
            "Given define o contexto inicial (pré-condições); "
            "When define a ação ou evento que ocorre; "
            "Then define o resultado esperado (comportamento observável)."
        ),
    },
    {
        "id": "bdd",
        "text": (
            "BDD (Behavior-Driven Development) é uma prática para descobrir, discutir "
            "e validar comportamentos esperados do sistema. "
            "BDD conecta requisitos de negócio e implementação técnica, "
            "permitindo que o sistema 'fale a língua do negócio'. "
            "BDD não é apenas sobre testes, é sobre construir entendimento compartilhado "
            "entre dev, QA e negócio. "
            "Cucumber é uma ferramenta que executa testes escritos em Gherkin, "
            "atuando como ponte entre negócio e código."
        ),
    },
    {
        "id": "integration_definition",
        "text": (
            "Teste de Integração verifica se componentes que funcionam isoladamente "
            "também funcionam corretamente quando integrados, respeitando: "
            "contratos, protocolos, fluxos de dados e efeitos colaterais. "
            "Entre os principais níveis de teste, testes de integração são os menos "
            "compreendidos e menos usados na prática. "
            "Pressupõe que todas as unidades já foram testadas separadamente. "
            "O objetivo é testar as interfaces entre os componentes."
        ),
    },
    {
        "id": "integration_strategies",
        "text": (
            "Estratégias de Integração baseadas em decomposição: "
            "Big-Bang: todas as unidades são integradas e testadas de uma única vez — "
            "problema: não há isolamento de faltas. "
            "Top-Down: integração inicia na raiz da árvore (main), unidades chamadas "
            "aparecem como stubs; vantagem: isolamento de faltas, adequado quando defeitos "
            "são prováveis nas camadas mais altas; desvantagem: grande esforço na criação de stubs. "
            "Bottom-Up: integração inicia nas folhas da árvore com drivers; "
            "vantagem: condições de teste mais simples; desvantagem: necessidade de drivers."
        ),
    },
    {
        "id": "integration_vs_unit",
        "text": (
            "Diferença entre Teste de Unidade e Teste de Integração: "
            "No teste de unidade, o repositório é em memória, sem dependências externas, "
            "ambiente totalmente controlado — falha indica erro no código. "
            "No teste de integração, o repositório usa banco real, envolve persistência, "
            "configuração e mapeamento — testa código mais infraestrutura, mais realista. "
            "Aspecto | Unidade | Integração: "
            "Dependência: Falsa/local vs Real; "
            "Infraestrutura: Não vs Sim; "
            "Velocidade: Alta vs Média; "
            "Tipo de falha: Código vs Integração."
        ),
    },
    {
        "id": "model_v",
        "text": (
            "O Modelo V relaciona fases de desenvolvimento com fases de teste. "
            "Especificação de Requisitos corresponde ao Teste de Aceitação. "
            "Projeto de Alto Nível corresponde ao Teste de Sistema. "
            "Projeto Detalhado corresponde ao Teste de Integração. "
            "Codificação corresponde ao Teste de Unidade. "
            "Cada fase de desenvolvimento planeja sua fase de teste correspondente."
        ),
    },
]


def retrieve_context(question: str, top_k: int = 3) -> list[str]:
    """
    Recuperação simples por palavras-chave.
    Em produção, substituir por embedding + busca vetorial.
    """
    question_lower = question.lower()

    keyword_map = {
        "acceptance_definition":    ["aceitação", "acceptance", "definição", "definition", "o que é"],
        "acceptance_vs_unit":       ["unidade", "unit", "diferença", "difference", "vs"],
        "acceptance_characteristics": ["característica", "characteristic", "não é", "not"],
        "acceptance_criteria":      ["critério", "criteria", "verificável", "verifiable"],
        "gherkin":                  ["gherkin", "given", "when", "then", "feature", "scenario"],
        "bdd":                      ["bdd", "behavior", "cucumber", "comportamento"],
        "integration_definition":   ["integração", "integration", "componente", "component"],
        "integration_strategies":   ["estratégia", "strategy", "big-bang", "top-down", "bottom-up", "stub", "driver"],
        "integration_vs_unit":      ["unidade", "unit", "diferença", "difference", "vs", "banco", "database"],
        "model_v":                  ["modelo v", "model v", "pirâmide", "níveis", "levels"],
    }

    scores = {}
    for chunk in CHUNKS:
        score = 0
        keywords = keyword_map.get(chunk["id"], [])
        for kw in keywords:
            if kw in question_lower:
                score += 1
        scores[chunk["id"]] = score

    sorted_chunks = sorted(CHUNKS, key=lambda c: scores[c["id"]], reverse=True)
    return [c["text"] for c in sorted_chunks[:top_k]]