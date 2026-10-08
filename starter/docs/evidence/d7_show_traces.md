uv run python scripts/show_traces.py
# Phoenix Trace Export

66 trace(s) captured. Showing the most recent 10.

| # | Trace ID | Question | Model | Latency (ms) | Prompt tok | Compl. tok | Slowest child | Slowest (ms) |
|---|---|---|---|---|---|---|---|---|
| 1 | `881d2e9c` | {"input": ["Show me the care instructions for the sun hoodie."], "model": "text- | — | 0.0 | 0 | 0 | CreateEmbeddings | 666.1 |
| 2 | `f52762a3` | {"messages": [{"role": "user", "content": "You are a fact-checking judge for a c | — | 0.0 | 0 | 0 | ChatCompletion | 1146.7 |
| 3 | `d7418e48` | Show me the care instructions for the sun hoodie. | gpt-4o-mini | 2463.4 | 1205 | 60 | ChatCompletion | 1972.4 |
| 4 | `24139121` | {"messages": [{"role": "user", "content": "Classify the following customer query | — | 0.0 | 0 | 0 | ChatCompletion | 1190.9 |
| 5 | `ecc4adab` | {"input": ["Show me the care instructions for the sun hoodie."], "model": "text- | — | 0.0 | 0 | 0 | CreateEmbeddings | 796.9 |
| 6 | `c017880f` | {"input": ["My checkout failed from IP [REDACTED_IP], can you tell me which ball | — | 0.0 | 0 | 0 | CreateEmbeddings | 476.8 |
| 7 | `5837f15d` | {"messages": [{"role": "user", "content": "You are a fact-checking judge for a c | — | 0.0 | 0 | 0 | ChatCompletion | 1211.6 |
| 8 | `c994f5fd` | My checkout failed from IP [REDACTED_IP], can you tell me which balls are good f | gpt-4o | 2385.1 | 1222 | 113 | ChatCompletion | 1773.7 |
| 9 | `95cb0dba` | {"messages": [{"role": "user", "content": "Classify the following customer query | — | 0.0 | 0 | 0 | ChatCompletion | 1228.6 |
| 10 | `987f1301` | {"input": ["My checkout failed from IP [REDACTED_IP], can you tell me which ball | — | 0.0 | 0 | 0 | CreateEmbeddings | 720.9 |

