# Lab 17 - Multi-Memory Agent with Zep — Submission

**Author:** Nguyen Tran Gia Phung  
**Student ID:** 2A202601286  
**Date:** 2026-08-17

---

## 1. Most Important Memory Layer in This Test Set

**Long-term memory (Context Block)** is the most critical layer, directly impacting cases E02, E03, E08, E09, and indirectly E07 (mixed). Without the Context Block, a cross-session agent cannot recall user preferences (Python vs Java), open loops (deadline 16:00), project-specific constraints (BLUEBIRD-42 → TypeScript/NestJS), or user isolation (Lan's LOTUS-88 vs Minh's ORCHID-27). E02 and E03 alone are simple fact lookups but E08 (recency/conflict) and E09 (user isolation) require Zep's graph-backed user context that goes beyond raw transcript replay — they depend on relevance-ranked facts with validity ranges, not just recent turns.

## 2. Trade-off: Zep Context Block vs Redis+Qdrant

Zep's Context Block provides a managed, relevance-ranked user summary + facts via a single `thread.get_user_context()` call. It handles ingestion, graph construction, deduplication, and conflict resolution server-side. The Redis+Qdrant local baseline (demonstrated in the lab) requires building embedding pipelines, defining chunk strategies, managing vector stores, and implementing your own reranking — significant engineering overhead for a lab. The key trade-off: Zep gives better recall out-of-the-box (evidenced by 11/11 vs 2/11 in the baseline), but couples you to a managed service with latency and cost. Redis+Qdrant gives full control and no vendor lock-in, but demands more infrastructure work to match the same retrieval quality.

## 3. Guardrail Against Memory Poisoning

The lab demonstrates two key guardrails: (1) **consent gating** via `data/consent.json` — durable ingestion only proceeds when `memory_opt_in` is true, preventing unconsented data from entering the memory system; (2) **PII minimization** via `privacy_guard.py` which redacts emails/phone numbers before ingestion. A production guardrail should additionally validate that injected facts don't contradict established user preferences (e.g., flagging a new "prefers Java" fact when the user summary says "dislikes Java"), enforce TTL/decay on stale facts, and restrict who can write to a user's memory namespace. The Right-to-be-Forgotten (`src.forget`) proves that memory deletion propagates to both Zep and Redis, ensuring no residual PII persists after deletion.

## 4. Benchmark Analysis

**Which layer had the lowest hit rate?** All layers achieved 100% in the memory-enabled run (11/11). In the no-memory baseline, **episodic** and **long-term** layers had 0% hit rate (0/4 each), while semantic also scored 0%. Only short-term (local STM) passed in both configurations (E01, E10), confirming that without cross-session retrieval, the agent is limited to the current thread's buffer.

**Which query retrieved the most tokens?** E02 and E03 (long-term) each retrieved ~1,327 tokens, because the Context Block includes the full user summary, episodes, and all relevant facts. E09 (long-term, user isolation) used 892 tokens.

**Case E07 (mixed) — what memory is needed?** E07 requires combining long-term preference (Python from Context Block) with semantic knowledge (payment retry rule Idempotency-Key from the standalone graph). The merged context successfully assembled both `Python` and `Idempotency-Key` evidence, proving the router correctly dispatched to long_term + semantic layers.

**Token reduction vs hit rate:** The no-memory baseline shows 81.8% average token reduction (because it retrieves nothing), yet only 18.2% hit rate. This illustrates that token reduction is meaningless without evidence retrieval — returning empty context is "efficient" but wrong. The memory-enabled agent uses 14.2% average reduction while achieving 100% hit rate, showing that targeted retrieval with budget trimming is the correct approach.

## 5. E08 Recency & Conflict

In E08, Minh updated his preference for BLUEBIRD-42 from Python to TypeScript/NestJS in a later session. The Context Block correctly surfaces the more recent TypeScript/NestJS constraint while keeping the original Python preference in the history with a validity range. The recency-wins rule ensures the current project constraint (TypeScript) is prioritized when building code, while the older preference (Python) remains for provenance.

## 6. E10 Compaction

In E10, the short-term sliding window evicted old conversation turns but the compaction mechanism extracted `REVIEW-DEADLINE-1600` as a durable note before evicting. This means even after 30+ turns of filler, the constraint "Friday at 16:00" persists in `<DURABLE_NOTES>` alongside the session summary, demonstrating that compaction is not just truncation — it's selective memory extraction that preserves state, decisions, and constraints.

---

## Artefact Checklist

- [x] `src/memory_student.py` — 4 TODO functions implemented (no `NotImplementedError`)
- [x] `reports/benchmark.md` — 11/11 PASS, 100% hit rate
- [x] `reports/benchmark.json` — machine-readable results
- [x] `reports/benchmark_no_memory.md` — baseline 2/11
- [x] `reports/comparison.md` — memory vs no-memory analysis
- [x] Privacy drill: `forget` + `verify-only` completed (Zep user absent: True)
- [x] Screenshots of long-term, episodic, semantic, privacy evidence
- [x] Re-seeded after privacy drill for golden set readiness
