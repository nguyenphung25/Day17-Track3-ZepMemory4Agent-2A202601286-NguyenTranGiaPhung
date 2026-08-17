# Lab 17 - Multi-Memory Agent với Zep

**Họ và tên:** Nguyễn Trần Gia Phụng

**MSSV:** 2A202601286

---

## 1. Phân tích Benchmark

| | Student | No-memory |
|---|---|---|
| Pass | **11/11 (100%)** | 2/11 (18.2%) |
| Latency TB | 748.5ms | 0.1ms |
| Giảm token TB | 12.9% | 81.8% |

- **Layer yếu nhất (no-memory):** long-term, episodic, semantic đều 0%. Chỉ short-term pass (E01, E10) vì evidence còn trong buffer.
- **Query nhiều token nhất:** E08 — 1,224 tokens (Context Block gồm summary + episodes + facts).
- **E07 (mixed):** cần long-term (Python preference) + semantic (Idempotency-Key). Router merge cả hai đúng.
- **Giảm token ≠ hit rate:** no-memory giảm 81.8% nhưng hit rate chỉ 18.2% — context rỗng thì "hiệu quả" nhưng sai.

## 2. Layer quan trọng nhất

**Long-term (Context Block).**

- Ảnh hưởng: E02, E03, E08, E09, gián tiếp E07.
- Không có nó → không nhớ preference, open loop, ràng buộc dự án.
- E08 cần recency-wins: Context Block surface TypeScript mới, giữ Python cũ kèm validity range.

## 3. Trade-off: Zep vs Redis+Qdrant

| | Zep | Redis+Qdrant |
|---|---|---|
| Ưu | 1 API call, xử lý server-side, đạt 11/11 ngay | Toàn quyền, không lock-in vendor |
| Nhược | Phụ thuộc dịch vụ, latency + chi phí | Phải tự xây pipeline, chunk, reranking |

## 4. Guardrail chống memory poisoning

3 cơ chế, đều đặt ở **write boundary** (lúc ingestion):

1. **Consent gating** — `require_memory_consent()` chặn user chưa opt-in.
2. **PII minimization** — `minimize_pii()` redact email/SĐT trước khi gửi Zep.
3. **Right-to-be-Forgotten** — `src.forget` xóa user khỏi Zep + Redis, verify xác nhận sạch.

**Vì sao write boundary?**

- Chặn ở write → dữ liệu chưa consent không bao giờ vào graph.
- Kiểm tra ở read → không undo được dữ liệu đã ingest.
- Redact ở write → áp dụng 1 lần, không thể đảo ngược. Redact ở read → phải scan mọi retrieval path.

## 5. E08 — Recency & Conflict

- Minh chuyển BLUEBIRD-42: Python → TypeScript/NestJS (session sau).
- Context Block: TypeScript `valid_at=2026-08-05`, Python cũ có `invalid_at`.
- Kết quả: recency wins, lịch sử giữ để truy vết.

## 6. E10 — Compaction

- 30+ turn filler → sliding window evict turn cũ.
- Compaction trích `REVIEW-DEADLINE-1600` vào `<DURABLE_NOTES>`.
- `messages_kept=6` nhưng constraint "thứ Sáu 16:00" vẫn còn.
- Kết luận: compaction = trích xuất có chọn lọc, không phải cắt bớt.
