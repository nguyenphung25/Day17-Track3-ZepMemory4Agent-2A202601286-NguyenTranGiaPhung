"""Probe what Zep returns for the 5 failing cases (G13, G15, G16, G18, G19)."""
import json, sys
sys.path.insert(0, "/workspace")
from src.config import settings
from src.zep_common import get_zep_client, render_graph_search
from src.utils import cap_query, load_knowledge

client = get_zep_client()
GRAPH = settings.semantic_graph_id
USER = "minh-lab17"

# Load queries from golden_eval_v3.json
with open("/workspace/data/golden_eval_v3.json", encoding="utf-8") as f:
    gc = json.load(f)["evaluations"]
queries = {c["id"]: c["query"] for c in gc}

# ── G16: long_term + semantic — missing LAB-REPORT-1600 ──
print("="*80, "\nG16 fact search (edges) for LAB-REPORT-1600")
q16 = cap_query(queries["G16"])
for scope in ("edges", "episodes", "nodes"):
    try:
        r = client.graph.search(user_id=USER, query=q16, scope=scope, limit=30)
        txt = render_graph_search(r)
        found = "lab-report-1600" in txt.lower()
        print(f"  {scope}: found={found}, len={len(txt)}")
        if found:
            for line in txt.split("\n"):
                if "1600" in line.lower():
                    print(f"    >>> {line[:300]}")
    except Exception as e:
        print(f"  {scope}: ERROR {e}")

# ── G18: episodic + semantic — missing connection churn + BUDGET-10-4-3-3 ──
print("\n" + "="*80, "\nG18 episodic search for connection churn")
q18 = cap_query(queries["G18"])
try:
    r = client.graph.search(user_id=USER, query=q18, scope="episodes", limit=30)
    txt = render_graph_search(r)
    found = "connection churn" in txt.lower() or "client" in txt.lower()
    print(f"  episodes: found_connection_churn={found}, len={len(txt)}")
    if "connection churn" in txt.lower():
        for line in txt.split("\n"):
            if "churn" in line.lower():
                print(f"    >>> {line[:300]}")
    else:
        # Show what IS there
        for i, line in enumerate(txt.split("\n")[:20]):
            print(f"    [{i}] {line[:200]}")
except Exception as e:
    print(f"  ERROR {e}")

print("\nG18 semantic search for BUDGET-10-4-3-3")
try:
    r = client.graph.search(graph_id=GRAPH, query=q18, scope="episodes", limit=30)
    txt = render_graph_search(r)
    found = "budget-10-4-3-3" in txt.lower()
    print(f"  episodes: found_budget={found}, len={len(txt)}")
    if "budget" in txt.lower():
        for line in txt.split("\n"):
            if "budget" in line.lower():
                print(f"    >>> {line[:400]}")
    # Also try scope=nodes
    r2 = client.graph.search(graph_id=GRAPH, query="context budget memory allocation layers percent", scope="episodes", limit=30)
    txt2 = render_graph_search(r2)
    found2 = "budget-10-4-3-3" in txt2.lower()
    print(f"  episodes (alt query): found={found2}, len={len(txt2)}")
except Exception as e:
    print(f"  ERROR {e}")

# ── G13: episodic + semantic — missing ClientSession ──
print("\n" + "="*80, "\nG13 episodic for ClientSession")
q13 = cap_query(queries["G13"])
try:
    r = client.graph.search(user_id=USER, query=q13, scope="episodes", limit=30)
    txt = render_graph_search(r)
    found = "clientsession" in txt.lower()
    print(f"  episodes: found={found}, len={len(txt)}")
    if not found:
        for i, line in enumerate(txt.split("\n")[:20]):
            print(f"    [{i}] {line[:200]}")
except Exception as e:
    print(f"  ERROR {e}")

# ── G19: long_term + episodic — missing ClientSession + ASYNC-FIX-20 ──
print("\n" + "="*80, "\nG19 long_term fact search for ClientSession + ASYNC-FIX-20")
q19 = cap_query(queries["G19"])
try:
    r = client.graph.search(user_id=USER, query=q19, scope="edges", limit=30)
    txt = render_graph_search(r)
    cs = "clientsession" in txt.lower()
    af = "async-fix-20" in txt.lower()
    print(f"  edges: found_ClientSession={cs}, found_ASYNC-FIX-20={af}, len={len(txt)}")
    for line in txt.split("\n"):
        if any(k in line.lower() for k in ("clientsession", "async-fix", "connection churn")):
            print(f"    >>> {line[:300]}")
except Exception as e:
    print(f"  ERROR {e}")

try:
    r = client.graph.search(user_id=USER, query=q19, scope="episodes", limit=30)
    txt = render_graph_search(r)
    cs = "clientsession" in txt.lower()
    af = "async-fix-20" in txt.lower()
    print(f"  episodes: found_ClientSession={cs}, found_ASYNC-FIX-20={af}, len={len(txt)}")
    if cs or af:
        for line in txt.split("\n"):
            if any(k in line.lower() for k in ("clientsession", "async-fix")):
                print(f"    >>> {line[:300]}")
except Exception as e:
    print(f"  ERROR {e}")

