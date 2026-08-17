# Lab 17 Golden Set Report

- Implementation: `student`
- Kind: `golden`
- Cases: **20**
- Passed: **20/20**
- Evidence hit rate: **100.0%**
- Average retrieval latency: **1025.2 ms**
- Average token reduction vs full source context: **2.5%**
- Golden bonus: **10/10** (100% required)

| Case | Layer | Pass | Latency ms | Retrieved tokens | Token reduction | Missing / Error |
| --- | --- | --- | ---: | ---: | ---: | --- |
| G01 | short_term | PASS | 0.3 | 227 | 0.0% |  |
| G02 | short_term | PASS | 0.1 | 133 | 0.0% |  |
| G06 | long_term | PASS | 1474.7 | 812 | 0.0% |  |
| G09 | semantic | PASS | 219.4 | 418 | 8.9% |  |
| G10 | semantic | PASS | 208.2 | 270 | 41.2% |  |
| G14 | mixed | PASS | 1642.4 | 1108 | 0.0% |  |
| G03 | long_term | PASS | 1382.9 | 1183 | 0.0% |  |
| G04 | long_term | PASS | 1422.5 | 1193 | 0.0% |  |
| G07 | episodic | PASS | 214.1 | 325 | 0.0% |  |
| G08 | episodic | PASS | 217.5 | 344 | 0.0% |  |
| G11 | mixed | PASS | 1545.8 | 1262 | 0.0% |  |
| G13 | mixed | PASS | 525.2 | 814 | 0.0% |  |
| G15 | mixed | PASS | 1909.5 | 1817 | 0.0% |  |
| G16 | mixed | PASS | 1629.7 | 1395 | 0.0% |  |
| G17 | mixed | PASS | 1560.1 | 1395 | 0.0% |  |
| G18 | mixed | PASS | 438.3 | 807 | 0.0% |  |
| G19 | mixed | PASS | 1607.0 | 1401 | 0.0% |  |
| G05 | long_term | PASS | 1308.7 | 1194 | 0.0% |  |
| G12 | mixed | PASS | 1632.5 | 1200 | 0.0% |  |
| G20 | mixed | PASS | 1565.4 | 1430 | 0.0% |  |

## Evidence excerpts

### G01 - short_term

`<SESSION_SUMMARY> user: Constraint HOLD-ALPHA-0900: standup is 09:00 sharp and must not be forgotten. | assistant: Noted standup constraint. | user: Constraint HOLD-BETA-STAGING: writes go to staging DB only. | assistant: Noted staging constraint. | user: Filler A about button padding. | assistant: Filler A. | user: Filler B about color tokens. | assistant: Filler B. | user: Filler C about copy tone. | assistant: Filler C. </SESSION_SUMMARY> <DURABLE_NOTES> - user: Constraint HOLD-ALPHA-0900: standup is 09:00 sharp and must not be forgotten. - assistant: Noted standup constraint. - user: Constraint HOLD-BETA-STAGING: writes go to staging DB only. - assistant: Noted staging constraint. </DURA`

### G02 - short_term

`<RECENT_TURNS> user: Ten du an ca nhan cua toi la ORCHID-27. Toi thich Python va khong thich Java. Khi giai thich code, hay dung vi du ngan. assistant: Da hieu: demo ca nhan ORCHID-27, uu tien Python, tranh Java, vi du ngan. user: Toi dang hoc async/await va hay nham coroutine voi Task. Neu sau nay gap chu de nay, hay giai thich bang timeline. assistant: Toi se uu tien timeline khi giai thich coroutine va Task. user: TODO: hoan thanh benchmark report truoc thu Sau luc 16:00. Day la open loop LAB-REPORT-1600. </RECENT_TURNS>`

### G06 - long_term

`<USER_SUMMARY> Lan Tran's main project is LOTUS-88. They prioritize Java and Spring Boot for backend examples.  Lan prefers to use Java and Spring Boot and explicitly avoids using Python in backend examples. </USER_SUMMARY>  <EPISODES> Episodes are source message or document excerpts shown in selection order.   - Created At: 2026-08-01 11:00:00     Source: message     Content: [user] {   "user_id": "lan-lab17",   "first_name": "Lan",   "last_name": "Tran",   "user_alias": "Lan Tran" }: Toi la Lan. Du an cua toi la LOTUS-88. Toi uu tien Java va Spring Boot, va khong dung Python trong vi du backend.   - Created At: 2026-08-01 11:00:20     Source: message     Content: Lab Assistant (assistant):`

### G09 - semantic

`EPISODE: {"id":"kb-payment-retry","entity":"Payment API Retry Policy","summary":"For POST /payments, every retryable request MUST send the same Idempotency-Key. Retry only HTTP 429 or transient 5xx errors, use exponential-backoff, and stop after max-3-retries. Marker: PAYMENT-RULE-3.","source":"internal-api-guideline-v3","updated_at":"2026-08-10T00:00:00Z"} metadata= EPISODE: For POST /payments, every retryable request MUST send the same Idempotency-Key. Retry only HTTP 429 or transient 5xx errors, use exponential-backoff, and stop after max-3-retries. Marker: PAYMENT-RULE-3. metadata= EPISODE: {"id":"kb-memory-privacy","entity":"Agent Memory Privacy Rule","summary":"Do not persist personal `

### G10 - semantic

`EPISODE: {"id":"kb-memory-privacy","entity":"Agent Memory Privacy Rule","summary":"Do not persist personal data without explicit opt-in. A deletion request must remove user-scoped memory and be verified across every store. Marker: DELETE-VERIFY-ALL.","source":"memory-governance-policy","updated_at":"2026-08-12T00:00:00Z"} metadata= EPISODE: Do not persist personal data without explicit opt-in. A deletion request must remove user-scoped memory and be verified across every store. Marker: DELETE-VERIFY-ALL. metadata= EPISODE: {"id":"kb-context-budget","entity":"Memory Context Budget","summary":"Reserve bounded context for memory. This lab uses short-term 10 percent, long-term 4 percent, episodi`

### G14 - mixed

`<LONG_TERM> <USER_SUMMARY> Lan Tran's main project is LOTUS-88. They prioritize Java and Spring Boot for backend examples.  Lan prefers to use Java and Spring Boot and explicitly avoids using Python in backend examples. </USER_SUMMARY>  <EPISODES> Episodes are source message or document excerpts shown in selection order.   - Created At: 2026-08-01 11:00:00     Source: message     Content: [user] {   "user_id": "lan-lab17",   "first_name": "Lan",   "last_name": "Tran",   "user_alias": "Lan Tran" }: Toi la Lan. Du an cua toi la LOTUS-88. Toi uu tien Java va Spring Boot, va khong dung Python trong vi du backend.   - Created At: 2026-08-01 11:00:20     Source: message     Content: Lab Assistant `

### G03 - long_term

`<USER_SUMMARY> The user is working on a personal project named ORCHID-27, which they prefer to use Python for. For the company project BLUEBIRD-42, the backend must be developed using TypeScript with NestJS, and Python is not to be used. The user is also debugging async HTTP requests for the ASYNC-FIX-20 incident. The solution involves reusing the aiohttp ClientSession and setting concurrency to 20, as the issue was connection churn, not the timeout threshold. A benchmark report for ORCHID-27 is due by Saturday at 16:00.  Minh Nguyen prefers Python and dislikes Java. When explaining code, use short examples. The user is learning about async/await and sometimes confuses coroutine with Task. I`

### G04 - long_term

`<USER_SUMMARY> The user is working on a personal project named ORCHID-27, which they prefer to use Python for. For the company project BLUEBIRD-42, the backend must be developed using TypeScript with NestJS, and Python is not to be used. The user is also debugging async HTTP requests for the ASYNC-FIX-20 incident. The solution involves reusing the aiohttp ClientSession and setting concurrency to 20, as the issue was connection churn, not the timeout threshold. A benchmark report for ORCHID-27 is due by Saturday at 16:00.  Minh Nguyen prefers Python and dislikes Java. When explaining code, use short examples. The user is learning about async/await and sometimes confuses coroutine with Task. I`

### G07 - episodic

`EPISODE: Minh con open loop hay deadline nao chua hoan thanh? EPISODE: Ten du an ca nhan cua toi la ORCHID-27. Toi thich Python va khong thich Java. Khi giai thich code, hay dung vi du ngan. EPISODE: Da hieu: demo ca nhan ORCHID-27, uu tien Python, tranh Java, vi du ngan. EPISODE: Toi dang hoc async/await va hay nham coroutine voi Task. Neu sau nay gap chu de nay, hay giai thich bang timeline. EPISODE: TODO: hoan thanh benchmark report truoc thu Sau luc 16:00. Day la open loop LAB-REPORT-1600. EPISODE: Hom nay toi debug async HTTP. Toi da thu tang timeout len 60s nhung van fail. EPISODE: Hay kiem tra connection pool, lifecycle cua client va concurrency. EPISODE: Cach hieu qua la reuse aiohtt`

### G08 - episodic

`EPISODE: Minh con open loop hay deadline nao chua hoan thanh? EPISODE: Ten du an ca nhan cua toi la ORCHID-27. Toi thich Python va khong thich Java. Khi giai thich code, hay dung vi du ngan. EPISODE: Toi dang hoc async/await va hay nham coroutine voi Task. Neu sau nay gap chu de nay, hay giai thich bang timeline. EPISODE: Toi se uu tien timeline khi giai thich coroutine va Task. EPISODE: TODO: hoan thanh benchmark report truoc thu Sau luc 16:00. Day la open loop LAB-REPORT-1600. EPISODE: Hom nay toi debug async HTTP. Toi da thu tang timeout len 60s nhung van fail. EPISODE: Hay kiem tra connection pool, lifecycle cua client va concurrency. EPISODE: Cach hieu qua la reuse aiohttp ClientSession`

### G11 - mixed

`<LONG_TERM> <USER_SUMMARY> The user is working on a personal project named ORCHID-27, which they prefer to use Python for. For the company project BLUEBIRD-42, the backend must be developed using TypeScript with NestJS, and Python is not to be used. The user is also debugging async HTTP requests for the ASYNC-FIX-20 incident. The solution involves reusing the aiohttp ClientSession and setting concurrency to 20, as the issue was connection churn, not the timeout threshold. A benchmark report for ORCHID-27 is due by Saturday at 16:00.  Minh Nguyen prefers Python and dislikes Java. When explaining code, use short examples. The user is learning about async/await and sometimes confuses coroutine `

### G13 - mixed

`<EPISODIC> EPISODE: Minh con open loop hay deadline nao chua hoan thanh? EPISODE: Ten du an ca nhan cua toi la ORCHID-27. Toi thich Python va khong thich Java. Khi giai thich code, hay dung vi du ngan. EPISODE: Backend cua BLUEBIRD-42 bat buoc dung stack gi? EPISODE: Da hieu: demo ca nhan ORCHID-27, uu tien Python, tranh Java, vi du ngan. EPISODE: Toi dang hoc async/await va hay nham coroutine voi Task. Neu sau nay gap chu de nay, hay giai thich bang timeline. EPISODE: Toi se uu tien timeline khi giai thich coroutine va Task. EPISODE: TODO: hoan thanh benchmark report truoc thu Sau luc 16:00. Day la open loop LAB-REPORT-1600. EPISODE: Hom nay toi debug async HTTP. Toi da thu tang timeout len`

### G15 - mixed

`<LONG_TERM> <USER_SUMMARY> The user is working on a personal project named ORCHID-27, which they prefer to use Python for. For the company project BLUEBIRD-42, the backend must be developed using TypeScript with NestJS, and Python is not to be used. The user is also debugging async HTTP requests for the ASYNC-FIX-20 incident. The solution involves reusing the aiohttp ClientSession and setting concurrency to 20, as the issue was connection churn, not the timeout threshold. A benchmark report for ORCHID-27 is due by Saturday at 16:00.  Minh Nguyen prefers Python and dislikes Java. When explaining code, use short examples. The user is learning about async/await and sometimes confuses coroutine `

### G16 - mixed

`<LONG_TERM> <USER_SUMMARY> The user is working on a personal project named ORCHID-27, which they prefer to use Python for. For the company project BLUEBIRD-42, the backend must be developed using TypeScript with NestJS, and Python is not to be used. The user is also debugging async HTTP requests for the ASYNC-FIX-20 incident. The solution involves reusing the aiohttp ClientSession and setting concurrency to 20, as the issue was connection churn, not the timeout threshold. A benchmark report for ORCHID-27 is due by Saturday at 16:00.  Minh Nguyen prefers Python and dislikes Java. When explaining code, use short examples. The user is learning about async/await and sometimes confuses coroutine `

### G17 - mixed

`<LONG_TERM> <USER_SUMMARY> The user is working on a personal project named ORCHID-27, which they prefer to use Python for. For the company project BLUEBIRD-42, the backend must be developed using TypeScript with NestJS, and Python is not to be used. The user is also debugging async HTTP requests for the ASYNC-FIX-20 incident. The solution involves reusing the aiohttp ClientSession and setting concurrency to 20, as the issue was connection churn, not the timeout threshold. A benchmark report for ORCHID-27 is due by Saturday at 16:00.  Minh Nguyen prefers Python and dislikes Java. When explaining code, use short examples. The user is learning about async/await and sometimes confuses coroutine `

### G18 - mixed

`<EPISODIC> EPISODE: Ten du an ca nhan cua toi la ORCHID-27. Toi thich Python va khong thich Java. Khi giai thich code, hay dung vi du ngan. EPISODE: Backend cua BLUEBIRD-42 bat buoc dung stack gi? EPISODE: Cuoi tuan minh ngoi mot minh lam demo rieng, khong hop team. Truoc khi chon template, nhac lai: khi lam viec ca nhan minh uu tien ngon ngu nao, va ma du an demo ca nhan la gi? Chi  EPISODE: Da hieu: demo ca nhan ORCHID-27, uu tien Python, tranh Java, vi du ngan. EPISODE: Toi dang hoc async/await va hay nham coroutine voi Task. Neu sau nay gap chu de nay, hay giai thich bang timeline. EPISODE: Toi se uu tien timeline khi giai thich coroutine va Task. EPISODE: TODO: hoan thanh benchmark repo`

### G19 - mixed

`<LONG_TERM> <USER_SUMMARY> The user is working on a personal project named ORCHID-27, which they prefer to use Python for. For the company project BLUEBIRD-42, the backend must be developed using TypeScript with NestJS, and Python is not to be used. The user is also debugging async HTTP requests for the ASYNC-FIX-20 incident. The solution involves reusing the aiohttp ClientSession and setting concurrency to 20, as the issue was connection churn, not the timeout threshold. A benchmark report for ORCHID-27 is due by Saturday at 16:00.  Minh Nguyen prefers Python and dislikes Java. When explaining code, use short examples. The user is learning about async/await and sometimes confuses coroutine `

### G05 - long_term

`<USER_SUMMARY> The user is working on a personal project named ORCHID-27, which they prefer to use Python for. For the company project BLUEBIRD-42, the backend must be developed using TypeScript with NestJS, and Python is not to be used. The user is also debugging async HTTP requests for the ASYNC-FIX-20 incident. The solution involves reusing the aiohttp ClientSession and setting concurrency to 20, as the issue was connection churn, not the timeout threshold. A benchmark report for ORCHID-27 is due by Saturday at 16:00.  Minh Nguyen prefers Python and dislikes Java. When explaining code, use short examples. The user is learning about async/await and sometimes confuses coroutine with Task. I`

### G12 - mixed

`<LONG_TERM> <USER_SUMMARY> The user is working on a personal project named ORCHID-27, which they prefer to use Python for. For the company project BLUEBIRD-42, the backend must be developed using TypeScript with NestJS, and Python is not to be used. The user is also debugging async HTTP requests for the ASYNC-FIX-20 incident. The solution involves reusing the aiohttp ClientSession and setting concurrency to 20, as the issue was connection churn, not the timeout threshold. A benchmark report for ORCHID-27 is due by Saturday at 16:00.  Minh Nguyen prefers Python and dislikes Java. When explaining code, use short examples. The user is learning about async/await and sometimes confuses coroutine `

### G20 - mixed

`<SHORT_TERM> <SESSION_SUMMARY> user: Constraint HOLD-ALPHA-0900: standup is 09:00 sharp and must not be forgotten. | assistant: Noted standup constraint. | user: Filler about dashboard widgets. | assistant: Filler. | user: Filler about CSS variables. | assistant: Filler. | user: Filler about copy review. | assistant: Filler. </SESSION_SUMMARY> <DURABLE_NOTES> - user: Constraint HOLD-ALPHA-0900: standup is 09:00 sharp and must not be forgotten. - assistant: Noted standup constraint. </DURABLE_NOTES> <RECENT_TURNS> user: Filler about empty charts. assistant: Filler. user: Filler about telemetry. assistant: Filler. user: Filler about a11y labels. assistant: Filler. </RECENT_TURNS> </SHORT_TERM>`
