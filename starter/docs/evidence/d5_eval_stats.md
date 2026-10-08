# Per-question distribution — make eval (top_k=5, 30 golden questions)

| metric | mean (aggregate) | median | p10 | p25 | min | max | NaN | rows < 0.5 |
|---|---|---|---|---|---|---|---|---|
| faithfulness | 0.918 | 1.000 | 0.667 | 0.947 | 0.500 | 1.000 | 0 | 0 |
| answer_relevancy | 0.835 | 0.847 | 0.608 | 0.785 | 0.365 | 1.000 | 0 | 1 |
| context_recall | 0.861 | 1.000 | 0.450 | 1.000 | 0.000 | 1.000 | 0 | 3 |
| context_precision | 0.732 | 1.000 | 0.000 | 0.535 | 0.000 | 1.000 | 0 | 8 |

`rows < 0.5` compares raw floats: RAGAS emits one context_precision of 0.49999999995 (a 0.5 after rounding), which is counted.

## Lowest context_precision questions

| context_precision | context_recall | faithfulness | question |
|---|---|---|---|
| 0.000 | 1.000 | 1.000 | Which paddle is lighter the Selkirk AMPED S2 or the JOOLA Hyperion CFS 16? |
| 0.000 | 1.000 | 0.947 | What shoes do you carry? |
| 0.000 | 0.500 | 0.667 | Which paddles have a fiberglass face? |
| 0.000 | 0.000 | 0.750 | What paddle would you recommend for someone who plays singles? |
| 0.000 | 0.000 | 0.667 | Which paddle has the widest body? |
| 0.000 | 0.000 | 0.500 | What is the cheapest product you sell? |
| 0.333 | 1.000 | 1.000 | What is the most expensive paddle you sell? |
| 0.500 | 1.000 | 1.000 | Compare the Selkirk Team Backpack and Franklin Sling Bag. |
