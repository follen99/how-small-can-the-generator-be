#!/usr/bin/env python3
"""Build the public dataset from the RagTester comparison exports.

Usage:
    python scripts/build_from_exports.py <C1 export.json> <C2 export.json>

Each export is the JSON produced by RagTester's "compare" view: a list of seven runs (one per
generator), each with `run_metadata` and 100 `results`. The script writes, for each corpus:

  data/golden/<corpus>.jsonl    the golden dataset: id, category, question, reference answer
  data/answers/<corpus>.jsonl   one record per (generator, question): answer, latency, tokens,
                                retrieved contexts with scores, judge scores
  data/runs.csv                 one row per run: generator, timestamp, embedding, top-k, judge,
                                hardware

It prints only counts and checks, never the content. Standard library only.
"""
import csv
import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CORPORA = ["c1_portfolio", "c2_synthetic_site"]
METRICS = ["answer_correctness", "faithfulness", "context_relevance", "answer_relevance"]
TEXT_KEYS = ("text", "content", "page_content", "document", "snippet")


def context_text(c):
    """Text of one retrieved context, whatever shape the export gives it."""
    if isinstance(c, str):
        return c
    if isinstance(c, dict):
        for k in TEXT_KEYS:
            if isinstance(c.get(k), str):
                return c[k]
    return ""


def build(corpus, export_path, runs_rows):
    runs = json.loads(Path(export_path).read_text(encoding="utf-8"))
    golden = None
    answers = []
    checks = Counter()
    for run in runs:
        meta, results = run["run_metadata"], run["results"]
        gen = meta["rag_model"].removeprefix("ollama/")
        g = sorted((r["id"], r["category"], r["query"], r["expected_answer"]) for r in results)
        if golden is None:
            golden = g
        elif g != golden:
            sys.exit(f"{corpus}: the runs do not share the same golden dataset ({gen})")
        runs_rows.append({
            "corpus": corpus, "generator": gen, "timestamp": meta["timestamp"],
            "embedding_model": meta["embedding_model"],
            "top_k": meta["retriever_config"].get("top_k"),
            "judge_model": meta["evaluator_model"].removeprefix("models/"),
            **{f"hw_{k}": v for k, v in meta.get("hardware_info", {}).items()},
        })
        for r in results:
            ev = r.get("evaluation") or {}
            ctx = r.get("retrieved_contexts") or []
            texts = [context_text(c) for c in ctx]
            checks["answers"] += 1
            checks["contexts_without_text"] += sum(1 for t in texts if not t.strip())
            checks[f"n_retrieved={r.get('n_retrieved')}"] += 1
            if not ev:
                checks["missing_evaluation"] += 1
            answers.append({
                "corpus": corpus,
                "generator": gen,
                "id": r["id"],
                "category": r["category"],
                "question": r["query"],
                "reference_answer": r["expected_answer"],
                "answer": r["generated_answer"],
                "latency_sec": r.get("latency_sec"),
                "output_tokens": r.get("output_token_count"),
                "retrieved_contexts": [
                    {"text": t, "score": s}
                    for t, s in zip(texts, (r.get("retrieval_scores") or []) + [None] * len(texts))
                ],
                "judge": {"model": ev.get("model", "").removeprefix("models/"),
                          **{m: ev.get(m) for m in METRICS}},
            })
    out_g = ROOT / "data" / "golden" / f"{corpus}.jsonl"
    with out_g.open("w", encoding="utf-8", newline="\n") as f:
        for i, cat, q, a in golden:
            f.write(json.dumps({"id": i, "category": cat, "question": q,
                                "reference_answer": a}, ensure_ascii=False) + "\n")
    out_a = ROOT / "data" / "answers" / f"{corpus}.jsonl"
    answers.sort(key=lambda x: (x["generator"], str(x["id"])))
    with out_a.open("w", encoding="utf-8", newline="\n") as f:
        for a in answers:
            f.write(json.dumps(a, ensure_ascii=False) + "\n")
    cats = Counter(c for _, c, _, _ in golden)
    print(f"{corpus}: {len(runs)} runs, {len(golden)} questions {dict(cats)}, "
          f"{checks['answers']} answers; checks: "
          + ", ".join(f"{k}={v}" for k, v in sorted(checks.items()) if k != "answers"))


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    (ROOT / "data" / "golden").mkdir(parents=True, exist_ok=True)
    (ROOT / "data" / "answers").mkdir(parents=True, exist_ok=True)
    rows = []
    for corpus, path in zip(CORPORA, sys.argv[1:]):
        build(corpus, path, rows)
    fields = sorted({k for r in rows for k in r}, key=lambda k: (k.startswith("hw_"), k))
    order = ["corpus", "generator", "timestamp", "embedding_model", "top_k", "judge_model"]
    fields = order + [f for f in fields if f not in order]
    with (ROOT / "data" / "runs.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(sorted(rows, key=lambda r: (r["corpus"], r["timestamp"])))
    print(f"runs.csv: {len(rows)} runs")


if __name__ == "__main__":
    main()
