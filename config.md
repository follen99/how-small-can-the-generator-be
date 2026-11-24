# Experimental configuration

Constant for all 14 runs (7 generators × 2 corpora). Per-run metadata, including hardware, is
in `data/runs.csv`.

| Item | Value |
|---|---|
| Chunking | semantic (Markdown hierarchy), 1,500 tokens |
| Embedding | `qwen3-embedding:0.6b` (Q8_0) |
| Vector store | Qdrant, local container |
| Retrieval | hybrid (dense + sparse BM25), top-K = 4, similarity threshold 0.25 |
| Generator call | stateless, same system prompt for every model (`prompts/`) |
| Judge | `gemini-3.1-flash-lite-preview`, single-answer grading against the reference answer, temperature 0.2 |
| Runtime | Ollama v0.20.7 |
| Hardware | AMD Ryzen 7 4800H, RTX 2060 Mobile 6 GiB, 16 GB DDR4, Pop!_OS 22.04 LTS |

<!-- DA VERIFICARE PRIMA DI PUBBLICARE: temperatura di generazione. Paper e tesi dicono 0.1;
     RAG-Maker ha RAG_TEMPERATURE = 0.6 in config.py in tutti i commit da aprile a luglio 2026,
     e RagTester non la invia. Controllare il checkout usato sul PC della campagna. Stesso
     controllo per CTX_WINDOW (default 8192). -->
| Generation temperature | **to be confirmed** |

## Generators

| Generator | Family | Parameters | Quantization | Execution |
|---|---|---|---|---|
| `gemma-4-31b-it` | Gemma 4 | 31B | FP16 | cloud API (reference) |
| `qwen3.5:4b` | Qwen3.5 | 4.7B | Q4_K_M | local |
| `phi3.5:3.8b` | Phi-3.5 | 3.8B | Q4_0 | local |
| `llama3.2:3b` | Llama 3.2 | 3.2B | Q4_K_M | local |
| `llama3.2:1b` | Llama 3.2 | 1.2B | Q8_0 | local |
| `qwen3.5:0.8b` | Qwen3.5 | 0.87B | Q8_0 | local |
| `tripolskypetr/gemma4-uncensored-aggressive` | Gemma 4 (safety removed) | 4.6B | Q2_K | local (control) |

## Code versions

The runs were produced with the authors' tools
[RAG-Maker](https://github.com/follen99/RAG-Maker) (builds the RAG system) and
[RagTester](https://github.com/follen99/RagTester) (runs the benchmark and the judge).

| Runs | Dates | RAG-Maker |
|---|---|---|
| C2: `gemma-4-31b-it`, `qwen3.5:4b`, `qwen3.5:0.8b`, `gemma4-uncensored` | 2026-05-17/18 | at or after `84fe65f` |
| C2: `llama3.2:1b`, `llama3.2:3b`, `phi3.5:3.8b`; all of C1 | 2026-07-23/27 | `21d9181` (branch `fix`) |

On C1, the `gemma4-uncensored` run was executed at a different time from the others and
received different chunks on 31 of the 100 questions (same chunks in a different order on 16
more, three chunks instead of four on one); every other run within a corpus received exactly
the same context for each question.
