# Prompts

Exact prompts used in the study (Italian for the generator, English for the judge).

| File | Role | Source |
|---|---|---|
| `generator_system_prompt.txt` | system message, identical for all seven generators | RAG-Maker, commit `21d9181`, `rag_pipeline/config.py` (`RAG_SYSTEM_PROMPT`) |
| `generator_user_template.txt` | user message: retrieved context + question | RAG-Maker, commit `21d9181`, `rag_pipeline/steps/step4_retrieve/chatbot.py` (`_augment_user`) |
| `judge_prompt.txt` | single-answer grading prompt of the LLM judge | RagTester, `app/services/evaluator.py` (`_EVAL_PROMPT`), unchanged since 2026-07-28 |

`{context}` is the concatenation of the retrieved chunks, each introduced by a header
`[Fonte i] <title> — <url>`. In the judge prompt, `{context_note}` is empty in this study: it
is filled only when the contexts carry no text, which never happened here.

Each generator call is stateless: no conversation history is carried between questions.
