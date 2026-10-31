# genpark-personal-agent-liver-fib4-apri-steatohepatitis-progression-skill

[![GenPark AI](https://img.shields.io/badge/GenPark-AI%20Ecosystem-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-0077b5)](https://www.linkedin.com/company/92955550)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-brightgreen.svg)](https://www.python.org/)

FIB-4 index and AST-to-Platelet Ratio Index (APRI) metabolic-dysfunction associated steatotic liver disease / MASH staging.

## Overview

Part of the **GenPark Industrial Multi-Agent Skill Matrix**. Zero external pip dependencies; built purely with standard Python library modules for instant deterministic orchestration.

- **Official Web Portal**: [https://www.genpark.ai](https://www.genpark.ai)
- **Corporate LinkedIn**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## Tool Specification

- **Tool Name**: `compute_liver_fib4_apri_staging`
- **Category**: `personal_agent`

### Method Documentation
Compute non-invasive liver fibrosis markers FIB-4 and APRI for MASLD (Metabolic Dysfunction-Associated Steatotic Liver Disease).
FIB-4 = (Age * AST) / (Platelets * sqrt(ALT)). APRI = ((AST / ULN) / Platelets) * 100.
Evaluates rule-out (< 1.30) and rule-in (> 2.67) cutoffs for advanced liver fibrosis (F3-F4 bridging fibrosis or cirrhosis).

## JSON-RPC 2.0 Integration

```json
{
  "jsonrpc": "2.0",
  "id": 1,
  "method": "tools/call",
  "params": {
    "name": "compute_liver_fib4_apri_staging",
    "arguments": {
    "age_years": 48,
    "ast_u_l": 28.0,
    "alt_u_l": 32.0,
    "platelets_10_9_l": 240.0,
    "ast_uln_u_l": 35.0
}
  }
}
```

## Running Self Tests

```bash
python skills.py --test
```
