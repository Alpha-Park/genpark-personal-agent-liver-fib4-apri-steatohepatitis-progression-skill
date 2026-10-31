# -*- coding: utf-8 -*-
"""GenPark Industrial Skill: genpark-personal-agent-liver-fib4-apri-steatohepatitis-progression-skill
Category: personal_agent
Website: https://www.genpark.ai
LinkedIn: https://www.linkedin.com/company/92955550
"""
import sys
import json
import math

sys.stdout.reconfigure(encoding="utf-8")

def compute_liver_fib4_apri_staging(age_years, ast_u_l, alt_u_l, platelets_10_9_l, ast_uln_u_l=35.0):
    if age_years <= 0 or ast_u_l <= 0 or alt_u_l <= 0 or platelets_10_9_l <= 0:
        raise ValueError("Clinical laboratory values must be positive numbers")
        
    fib4 = (age_years * ast_u_l) / (platelets_10_9_l * math.sqrt(alt_u_l))
    apri = ((ast_u_l / ast_uln_u_l) / platelets_10_9_l) * 100.0
    
    # FIB-4 standard AASLD/EASL thresholds:
    # Low risk (F0-F1, NPV > 90%): < 1.30 (or < 2.0 in age > 65)
    # High risk (F3-F4, PPV > 65%): > 2.67
    low_cutoff = 2.0 if age_years >= 65 else 1.30
    
    if fib4 < low_cutoff:
        risk_category = "LOW_RISK_F0_F1"
        action = "High negative predictive value (>90%) for advanced fibrosis. Primary care lifestyle management."
        referral_indicated = False
    elif fib4 > 2.67:
        risk_category = "HIGH_RISK_F3_F4"
        action = "High probability of advanced fibrosis/cirrhosis. Urgent hepatology referral for elastography (VCTE/FibroScan) or liver biopsy."
        referral_indicated = True
    else:
        risk_category = "INDETERMINATE_RISK_F2"
        action = "Indeterminate zone. Second-line non-invasive testing (Enhanced Liver Fibrosis ELF test or transient elastography) advised."
        referral_indicated = True
        
    return {
        "fib4_index": round(fib4, 2),
        "apri_index": round(apri, 2),
        "platelet_count_10_9_l": platelets_10_9_l,
        "ast_to_alt_ratio": round(ast_u_l / alt_u_l, 2),
        "fibrosis_risk_tier": risk_category,
        "clinical_action": action,
        "specialist_referral_recommended": referral_indicated
    }


def handle_rpc(request_str):
    try:
        req = json.loads(request_str)
        rpc_id = req.get("id")
        method = req.get("method")
        params = req.get("params", {})
        
        if method == "tools/list":
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "tools": [{
                        "name": "compute_liver_fib4_apri_staging",
                        "description": """Compute non-invasive liver fibrosis markers FIB-4 and APRI for MASLD (Metabolic Dysfunction-Associated Steatotic Liver Disease).
FIB-4 = (Age * AST) / (Platelets * sqrt(ALT)). APRI = ((AST / ULN) / Platelets) * 100.
Evaluates rule-out (< 1.30) and rule-in (> 2.67) cutoffs for advanced liver fibrosis (F3-F4 bridging fibrosis or cirrhosis).""",
                        "inputSchema": {
                            "type": "object",
                            "properties": {}
                        }
                    }]
                }
            })
        elif method == "tools/call":
            call_params = params.get("arguments", {})
            res = compute_liver_fib4_apri_staging(**call_params)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "result": {
                    "content": [{
                        "type": "text",
                        "text": json.dumps(res, indent=2)
                    }]
                }
            })
        else:
            return json.dumps({
                "jsonrpc": "2.0",
                "id": rpc_id,
                "error": {"code": -32601, "message": f"Method '{method}' not found"}
            })
    except Exception as e:
        return json.dumps({
            "jsonrpc": "2.0",
            "id": None,
            "error": {"code": -32000, "message": str(e)}
        })

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "--test":
        sample = {'age_years': 48, 'ast_u_l': 28.0, 'alt_u_l': 32.0, 'platelets_10_9_l': 240.0, 'ast_uln_u_l': 35.0}
        out = compute_liver_fib4_apri_staging(**sample)
        print("[TEST_PASS] Output:", json.dumps(out))
    else:
        for line in sys.stdin:
            line = line.strip()
            if not line:
                continue
            print(handle_rpc(line))
