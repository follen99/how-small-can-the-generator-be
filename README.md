<!-- DA COMPLETARE PRIMA DI PUBBLICARE (poi togliere questo blocco):
     1. temperatura di generazione in config.md (0.1 o 0.6?);
     2. riferimento bibliografico del paper una volta accettato. -->

# How Small Can the Generator Be? — data and materials

Data and materials for the paper *How Small Can the Generator Be? An Empirical Study of Small
Language Models in Local Retrieval-Augmented Generation* (G. Ranauro, D. A. Tamburri, University
of Sannio; under review at IEEE Transactions on Knowledge and Data Engineering).

The study holds a RAG pipeline constant (retrieval, prompt, golden dataset and judge) and varies
only the generator: six local models from 0.87B to 4.7B parameters, a control model with its
safety layers removed, and a 31B cloud reference, on two Italian corpora with 100 questions
each. Every question is answerable by construction, except the negation ones, whose correct
answer is to abstain.

## Contents

| Path | What it is |
|---|---|
| `data/golden/` | the two golden datasets: 100 questions each, with reference answer and category |
| `data/answers/` | the 1,400 generated answers (7 generators × 2 corpora × 100), with latency, output tokens, the retrieved chunks and their similarity scores, and the judge's four scores |
| `data/runs.csv` | one row per run: generator, timestamp, embedding model, top-K, judge, hardware |
| `prompts/` | the exact generator and judge prompts |
| `config.md` | pipeline parameters, generators and code versions |
| `corpora/c1_portfolio/` | pointer to the first corpus (a public portfolio site), with the exact commit used |
| `corpora/c2_synthetic_site/` | the second corpus: a synthetic site about a fictional company |
| `scripts/build_from_exports.py` | rebuilds `data/` from the benchmark tool's exports |
| `LICENSE-DATA`, `LICENSE-CODE` | licenses (CC BY 4.0, MIT) |

All questions, reference answers and generated answers are in Italian.

## Data format

`data/golden/<corpus>.jsonl`, one question per line:

```json
{"id": "...", "category": "standard | factual | reformulation | multi_hop | negation",
 "question": "...", "reference_answer": "..."}
```

`data/answers/<corpus>.jsonl`, one answer per line:

```json
{"corpus": "c1_portfolio", "generator": "llama3.2:3b", "id": "...", "category": "...",
 "question": "...", "reference_answer": "...", "answer": "...",
 "latency_sec": 0.0, "output_tokens": 0,
 "retrieved_contexts": [{"text": "...", "score": 0.0}],
 "judge": {"model": "gemini-3.1-flash-lite-preview", "answer_correctness": 0,
           "faithfulness": 0, "context_relevance": 0, "answer_relevance": 0}}
```

Judge scores are integers from 0 to 100. How they are aggregated into the quality measure
reported in the paper is described there.

## Rebuilding the data

```bash
python scripts/build_from_exports.py <C1 export.json> <C2 export.json>
```

The exports are the comparison files produced by RagTester. The script uses the standard
library only and prints counts and consistency checks, not content.

## License

- Data, prompts, corpora and documentation: [CC BY 4.0](LICENSE-DATA).
- Code in `scripts/`: [MIT](LICENSE-CODE).

The C1 corpus is the first author's public portfolio site; its content, including the personal
information it contains, is published here with the author's consent.
