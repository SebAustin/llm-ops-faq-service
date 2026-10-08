# Per-span breakdown — trace `e31b78a44f117bafedf215619096a624`

Question: 'Compare the moisture-wicking and durability properties of the apparel options you sell.'  
Model: None · total (root `rag_query`) = **3721.9 ms**

| span | kind | start offset (ms) | duration (ms) | % of rag_query |
|---|---|---|---|---|
| rag_query | UNKNOWN | 0.0 | 3721.9 | 100.0% |
| CreateEmbeddings | EMBEDDING | 0.3 | 558.7 | 15.0% |
| ChatCompletion | LLM | 575.4 | 3138.7 | 84.3% |
| rag_generation | UNKNOWN | 3718.7 | 0.0 | 0.0% |

## Sibling traces for the same request (classification, cache-lookup embedding, hallucination judge)

| trace | root span | first input chars | start offset vs rag_query (ms) | duration (ms) |
|---|---|---|---|---|
| `7cb0c45d` | CreateEmbeddings | {"input": ["What material are the Engage Court Shorts made o | -7053 | 740.1 |
| `8dd3eee5` | ChatCompletion | {"messages": [{"role": "user", "content": "Classify the foll | -6305 | 1116.7 |
| `3c1cbc0c` | rag_query | What material are the Engage Court Shorts made of? | -5186 | 1704.9 |
| `85acaad8` | ChatCompletion | {"messages": [{"role": "user", "content": "You are a fact-ch | -3475 | 1130.1 |
| `8e623f3b` | CreateEmbeddings | {"input": ["What material are the Engage Court Shorts made o | -2102 | 523.0 |
| `1b9d9e2e` | CreateEmbeddings | {"input": ["Compare the moisture-wicking and durability prop | -1406 | 497.0 |
| `0a091851` | ChatCompletion | {"messages": [{"role": "user", "content": "Classify the foll | -899 | 896.2 |
| `a1a27634` | ChatCompletion | {"messages": [{"role": "user", "content": "You are a fact-ch | 3726 | 1262.3 |
| `01fdba0f` | CreateEmbeddings | {"input": ["Compare the moisture-wicking and durability prop | 5423 | 481.5 |
