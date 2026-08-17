# Lab 17 - Multi-Memory Agent với Zep: Tài liệu Tổng quan

## 1. Kiến trúc Tổng quan

```
                    ┌─────────────────────────────┐
                    │     control_plane/*.md       │
                    │  persona / rules / schema    │
                    └──────────────┬──────────────┘
                                   │
JSON sessions ──────► LangGraph Router ──────► retrieve(query)
                                   │
        ┌──────────────────────────┼───────────────────────────┐
        │                          │                           │
   Short-term                 Zep User Graph              Zep Standalone Graph
   buffer/summary/          Long-term + Episodes         Semantic/Domain KB
   sliding window            Context / Facts              │
        │                    └──────────────────────────────┘
        └──────────────────────────┼───────────────────────────┘
                                   │
                         Priority + Token Budget
                                   │
                            Merged Context
                                   │
                    Evaluator / Demo Agent
```

---

## 2. 4 Memory Layer và Cách hoạt động

### 2.1. Short-term Memory (Local)

**Mục đích:** Ghi nhớ nội dung trong session hiện tại.

**Cách hoạt động:**
- Dùng `ShortTermMemory` trong `src/short_term.py`
- 3 strategy: `buffer` (giữ hết), `summary` (cô đặc), `sliding` (cửa sổ trượt) — lab dùng `sliding`
- Khi số tin nhắn > `max_recent_messages` (6), tự động compact:
  1. Extract durable notes (todo, deadline, constraint, marker `ORCHID-27`, etc.)
  2. Giữ lại K tin nhắn gần nhất
  3. Tổng hợp phần cũ thành `<SESSION_SUMMARY>`

**Flow render:**
```
<SESSION_SUMMARY>
  user: TODO: hoàn thành benchmark report trước thứ Sáu lúc 16:00...
</SESSION_SUMMARY>
<DURABLE_NOTES>
  - user: Constraint: REVIEW-DEADLINE-1600...
</DURABLE_NOTES>
<RECENT_TURNS>
  user: Filler turn 4...
  assistant: Filler answer 4...
</RECENT_TURNS>
```

**Test case:** E01, E10

---

### 2.2. Long-term Memory (Zep Context Block)

**Mục đích:** Nhớ facts/preferences跨 sessions — "Minh thích Python", "BLUEBIRD-42 dùng TypeScript".

**Cách hoạt động (TODO 1 trong `memory_student.py`):**
```python
# 1. Tạo thread evaluation mới
prime_eval_thread(client, user_id, thread_id, query)

# 2. Lấy Context Block từ Zep
user_context = client.thread.get_user_context(thread_id=thread_id)
context_block = user_context.context  # string

# 3. Bonus: tìm facts với validity range
facts = client.graph.search(user_id=user_id, query=cap_query(query), scope="edges", limit=20)
fact_text = render_graph_search(facts)

# 4. Kết hợp
return join_nonempty([context_block, fact_text])
```

**Zep làm gì ở backend:**
```
user.add() → thread.create() → thread.add_messages() → Zep graph ingestion
                                                          ↓
                                          User Graph (facts + summary + episodes)
                                                          ↓
                              thread.get_user_context(thread_id) → Context Block
```

**Context Block chứa:**
- `<USER_SUMMARY>`: Tóm tắt preference/project
- `<EPISODES>`: Message excerpts theo relevance
- Facts với validity ranges (phục vụ recency check)

**Test case:** E02, E03, E08, E09

---

### 2.3. Episodic Memory (User Graph Search)

**Mục đích:** Tìm "lần trước đã làm gì" — trajectory, reflection, lessons learned.

**Cách hoạt động (TODO 2 trong `memory_student.py`):**
```python
results = client.graph.search(
    user_id=user_id,           # ← user-scoped, KHÔNG phải graph_id
    query=cap_query(query),
    scope="episodes",          # ← lấy raw message episodes
    limit=15,
)
return render_graph_search(results, episode_char_cap=180)
```

**Phân biệt scopes:**
| Scope | Trả về | Dùng cho |
|---|---|---|
| `episodes` | Raw message content | Episodic recall |
| `edges` | Facts với validity range | Long-term fact check |
| `nodes` | Entity summaries | Semantic KB |

**Test case:** E04, E05

---

### 2.4. Semantic Memory (Standalone Graph)

**Mục đích:** Tri thức domain dùng chung — "quy tắc retry payment", "incident playbook".

**Cách hoạt động (TODO 3 trong `memory_student.py`):**
```python
results = client.graph.search(
    graph_id=semantic_graph_id,  # ← KHÔNG phải user_id
    query=cap_query(query),
    scope="episodes",            # ← giữ marker literal (PAYMENT-RULE-3)
    limit=8,
)
return render_graph_search(results)
```

**Tại sao dùng `scope="episodes"` thay vì `"auto"`:**
- `"auto"` trả về extracted facts → **mất marker codes** (`PAYMENT-RULE-3`, `CONN-POOL-FIRST`)
- `"episodes"` trả về raw document text → giữ nguyên markers

**Knowledge source:** `data/knowledge.jsonl` — domain KB seed vào standalone graph

**Test case:** E06, E11

---

## 3. Context Assembly & Token Budget

### TODO 4: `assemble_context`

```python
def assemble_context(self, layers: dict[str, str]) -> tuple[str, dict[str, dict[str, int]]]:
    return self.budget.assemble(layers)
```

### Budget Ratio (10/4/3/3)

| Layer | Budget | Token Limit (8000 ctx) |
|---|---|---|
| short_term | 10% | 800 tokens |
| long_term | 4% | 320 tokens |
| episodic | 3% | 240 tokens |
| semantic | 3% | 240 tokens |

### Priority Order
```
1. short-term      ← Luôn ưu tiên
2. long-term        ← Facts/preferences
3. episodic         ← Trajectory/experience
4. semantic         ← Domain knowledge
```

### Flow Assembly
```
layers = {
    "short_term": "...",
    "long_term": "...",
    "episodic": "...",
    "semantic": "..."
}
        ↓
Priority loop: short_term → long_term → episodic → semantic
        ↓
Trim each layer: text[:max_chars] + "\n[...trimmed...]"
        ↓
Wrap: <SHORT_TERM>...</SHORT_TERM>\n\n<LONG_TERM>...</LONG_TERM>...
        ↓
return (merged_text, breakdown_dict)
```

---

## 4. Benchmark Flow

### 4.1. Evaluator (`src/evaluate.py`)

```
For each case in E01-E11:
    1. Determine layer (short_term / long_term / episodic / semantic / mixed)
    2. Route to correct retrieval function:
       - short_term → ShortTermMemory.render() (local)
       - long_term  → memory_impl.retrieve_long_term()
       - episodic   → memory_impl.retrieve_episodic()
       - semantic   → memory_impl.retrieve_semantic()
       - mixed      → retrieve long_term + semantic → assemble_context()
    3. Score: check must_contain_all markers in retrieved text
    4. PASS if ALL markers found AND no forbidden markers
```

### 4.2. Scoring Logic
```python
def score_case(case, retrieved):
    text = normalize(retrieved)  # lowercase + collapse whitespace
    missing = [m for m in case["must_contain_all"] if normalize(m) not in text]
    forbidden = [f for f in case.get("must_not_contain", []) if normalize(f) in text]
    return (not missing and not forbidden), missing, forbidden
```

---

## 5. Cài đặt (Implementation) — `memory_student.py`

### TODO 1/4: retrieve_long_term

```python
def retrieve_long_term(self, user_id, thread_id, query):
    # Bước 1: Tạo thread evaluation
    prime_eval_thread(self.client, user_id, thread_id, query)

    # Bước 2: Lấy Context Block
    user_context = self.client.thread.get_user_context(thread_id=thread_id)
    context_block = getattr(user_context, "context", "") or ""

    # Bước 3: Bonus — graph edge search cho transparency
    try:
        facts = self.client.graph.search(
            user_id=user_id,
            query=cap_query(query),  # cap_query防止Zep reject (>400 chars)
            scope="edges",
            limit=20,
        )
        fact_text = render_graph_search(facts)
    except Exception:
        fact_text = ""

    # Bước 4: Kết hợp
    return join_nonempty([context_block, fact_text], sep="\n\n")
```

**Lưu ý:**
- `cap_query(query)`: Zep reject queries > 400 chars
- `scope="edges"`: Trả về facts với `valid_at`/`invalid_at` — phục vụ recency check

---

### TODO 2/4: retrieve_episodic

```python
def retrieve_episodic(self, user_id, query):
    results = self.client.graph.search(
        user_id=user_id,           # User-scoped!
        query=cap_query(query),
        scope="episodes",
        limit=15,
    )
    return render_graph_search(results, episode_char_cap=180)
```

**Lưu ý:**
- `episode_char_cap=180`: Cắt mỗi episode xuống 180 chars để nhiều episode hơn trong budget
- Nếu không cap, 1-2 verbose episodes sẽ chiếm hết budget

---

### TODO 3/4: retrieve_semantic

```python
def retrieve_semantic(self, graph_id, query):
    q = cap_query(query)
    try:
        results = self.client.graph.search(
            graph_id=graph_id,      # Standalone graph, KHÔNG phải user_id
            query=q,
            scope="episodes",       # Giữ marker literal
            limit=8,
        )
    except Exception:
        # Fallback cho SDK version khác
        results = self.client.graph.search(
            graph_id=graph_id,
            query=q,
            scope="nodes",
            limit=8,
        )
    return render_graph_search(results)
```

**Lưu ý:**
- `graph_id=semantic_graph_id` từ config (vinuni-lab17-domain-kb)
- `scope="nodes"` là fallback khi `scope="episodes"` không khả dụng

---

### TODO 4/4: assemble_context

```python
def assemble_context(self, layers):
    return self.budget.assemble(layers)
```

`ContextBudgetManager.assemble()` tự xử lý:
1. Loop priority: short_term → long_term → episodic → semantic
2. Trim mỗi layer theo budget (10/4/3/3)
3. Wrap mỗi layer trong XML tags
4. Return `(merged_text, breakdown_dict)`

---

## 6. Các Case Test và Kết quả

### Practice Set (11 cases)

| Case | Layer | Query | Markers | Kết quả |
|---|---|---|---|---|
| E01 | short_term | Tên dự án cá nhân tôi vừa nhắc là gì? | `ORCHID-27` | PASS |
| E02 | long_term | Võ demo cá nhân của Minh, ngôn ngữ ưu tiên là gì? | `Python` | PASS |
| E03 | long_term | Minh còn open loop hay deadline nào chưa hoàn thành? | `benchmark report`, `16:00` | PASS |
| E04 | episodic | Lần trước Minh fix async HTTP timeout bằng cách nào? | `ClientSession`, `concurrency=20`, `ASYNC-FIX-20` | PASS |
| E05 | episodic | Reflection của sự cố async là gì, tăng timeout có phải root fix không? | `connection churn`, `timeout threshold` | PASS |
| E06 | semantic | Quy tắc retry POST payment là gì? | `Idempotency-Key`, `max-3-retries`, `exponential-backoff` | PASS |
| E07 | mixed | Hãy chọn hướng dẫn code retry payment phù hợp với preference cá nhân của Minh. | `Python`, `Idempotency-Key` | PASS |
| E08 | long_term | Backend của BLUEBIRD-42 bắt buộc dùng stack gì? | `BLUEBIRD-42`, `TypeScript`, `NestJS` | PASS |
| E09 | long_term | Lan ưu tiên stack backend nào cho LOTUS-88? | `LOTUS-88`, `Java`, `Spring Boot` | PASS |
| E10 | short_term | Deadline review cũ là khi nào? | `REVIEW-DEADLINE-1600`, `Friday`, `16:00` | PASS |
| E11 | semantic | Theo incident playbook, trước khi tăng timeout cần kiểm tra gì? | `connection pooling`, `CONN-POOL-FIRST` | PASS |

### Kết quả Benchmark

| Metric | Student | No-Memory |
|---|---|---|
| Hit rate | **11/11 (100%)** | 2/11 (18.2%) |
| Avg latency | 1826.5ms | 0.4ms |
| Token reduction | 14.2% | 81.8% |

---

## 7. Flow Chi tiết từng Phase

### Phase A: Short-term (30 phút)

```
1. docker compose run --rm app python -m src.demo_short_term
   ↓
2. Quan sát 3 strategy: buffer / summary / sliding
   ↓
3. Sửa max_recent_messages: 6 → 4
   ↓
4. Verify: REVIEW-DEADLINE-1600 vẫn còn trong DURABLE_NOTES
```

### Phase B: Long-term (40 phút)

```
1. Viết retrieve_long_term trong memory_student.py
   ↓
2. docker compose run --rm app python -m src.evaluate --impl student --reuse-seeded --only-layer long_term
   ↓
3. Verify: E02 (Python), E03 (benchmark report + 16:00), E08 (BLUEBIRD-42 + TypeScript + NestJS), E09 (LOTUS-88 + Java + Spring Boot)
```

### Phase C: Episodic (20 phút)

```
1. Viết retrieve_episodic
   ↓
2. docker compose run --rm app python -m src.evaluate --impl student --reuse-seeded --only-layer episodic
   ↓
3. Verify: E04 (ClientSession + concurrency=20 + ASYNC-FIX-20), E05 (connection churn + timeout threshold)
```

### Phase D: Semantic (20 phút)

```
1. Viết retrieve_semantic
   ↓
2. docker compose run --rm app python -m src.evaluate --impl student --reuse-seeded --only-layer semantic
   ↓
3. Verify: E06 (Idempotency-Key + max-3-retries + exponential-backoff), E11 (connection pooling + CONN-POOL-FIRST)
```

### Phase E: Router + Budget + Benchmark (30 phút)

```
1. Viết assemble_context
   ↓
2. Chạy baseline: docker compose run --rm app python -m src.evaluate --impl no_memory
   ↓
3. Chạy student: docker compose run --rm app python -m src.evaluate --impl student --reuse-seeded
   ↓
4. So sánh: docker compose run --rm app python -m src.compare_reports
   ↓
5. Verify: reports/benchmark.md, reports/benchmark_no_memory.md, reports/comparison.md
```

### Privacy Drill (15 phút)

```
1. docker compose run --rm app python -m src.forget --user-id minh-lab17
   ↓
2. docker compose run --rm app python -m src.forget --user-id minh-lab17 --verify-only
   ↓
3. Verify: Zep user absent: True, Redis user keys remaining: 0
```

---

## 8. Lưu ý Quan trọng

### cap_query()
Zep reject queries > 400 chars. Luôn wrap query:
```python
from .utils import cap_query
q = cap_query(query)
```

### User vs Graph ID
| Hàm | Dùng | Ví dụ |
|---|---|---|
| `retrieve_long_term` | `user_id` + `thread_id` | Context Block |
| `retrieve_episodic` | `user_id` | User graph search |
| `retrieve_semantic` | `graph_id` (standalone) | Domain KB |

### Scope Selection
| Scope | Nội dung | Dùng cho |
|---|---|---|
| `"episodes"` | Raw message text | Episodic + Semantic (giữ markers) |
| `"edges"` | Facts + validity ranges | Long-term fact check |
| `"auto"` | Extracted facts | ❌ Mất marker codes |
| `"nodes"` | Entity summaries | Fallback |

### Privacy
- `consent.json`: Yêu cầu opt-in trước khi durable ingestion
- `privacy_guard.py`: Redact email/phone trước khi ingest
- `src.forget`: Xóa user + Redis keys, giữ shared semantic KB

---

## 9. File Structure

```
Day17-Track3-ZepMemory4Agent-2A202601286-NguyenTranGiaPhung/
├── .env                    # ZEP_API_KEY, GEMINI_API_KEY
├── docker-compose.yml      # Redis + Qdrant + app
├── Dockerfile
├── data/
│   ├── sessions.json       # Synthetic user sessions
│   ├── knowledge.jsonl     # Domain KB (semantic graph seed)
│   ├── consent.json        # Privacy consent registry
│   └── ground_truth.json   # Ground truth for practice set
├── src/
│   ├── memory_student.py   # ← STUDENT CODE (4 TODOs)
│   ├── memory_reference.py # Reference implementation
│   ├── short_term.py       # ShortTermMemory class
│   ├── context_budget.py   # ContextBudgetManager (10/4/3/3)
│   ├── zep_common.py       # Zep client + helpers
│   ├── evaluate.py         # Benchmark runner
│   ├── seed.py             # One-time Zep seed
│   ├── smoke.py            # Infrastructure check
│   ├── forget.py           # Privacy drill
│   ├── compare_reports.py  # Memory vs no-memory
│   ├── router.py           # Query routing hints
│   ├── config.py           # Settings from .env
│   └── utils.py            # cap_query, estimate_tokens, etc.
├── reports/
│   ├── benchmark.json      # Student results (machine)
│   ├── benchmark.md        # Student results (human)
│   ├── benchmark_no_memory.json
│   ├── benchmark_no_memory.md
│   └── comparison.md
└── README_submission.md    # Written analysis
```

---

## 10. Commands Reference

```bash
# Setup
cp .env.example .env
docker compose build
docker compose up -d redis qdrant

# Infrastructure check
docker compose run --rm app python -m src.smoke

# Seed (one-time, takes ~5 min)
docker compose run --rm app python -m src.seed

# Benchmark - student
docker compose run --rm app python -m src.evaluate --impl student --reuse-seeded

# Benchmark - no memory baseline
docker compose run --rm app python -m src.evaluate --impl no_memory

# Compare
docker compose run --rm app python -m src.compare_reports

# Privacy drill
docker compose run --rm app python -m src.forget --user-id minh-lab17
docker compose run --rm app python -m src.forget --user-id minh-lab17 --verify-only

# Re-seed after forget (for golden set)
docker compose run --rm app python -m src.seed

# Golden set (when instructor releases)
docker compose run --rm app python -m src.evaluate --impl student --reuse-seeded --golden

# Unit tests
docker compose run --rm app pytest -q
```
