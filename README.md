# First-Principles Admissibility Framework

A structural claim auditor.

> Does not ask: "Does this sound right?"
> Asks: **"What breaks first, and was that break declared before movement?"**

## Core Rule

```
Possible ≠ Repeatable ≠ Scalable ≠ Transferable ≠ Admissible
```

A claim has not earned movement until it declares: what carries it, where it holds, what it costs, how it transfers, how it fails, who repairs it, what budget preserves it.

## Five Audit Layers

| Layer | Question | Key Failure Signature |
|-------|----------|-----------------------|
| 1. False Closure | Did the claim close too early? | FALSE_CLOSURE |
| 2. First-Principles Admissibility F(X)={P,S,T,D} | Can it exist, repeat, transfer, and endure? | POSSIBLE_ONCE_SYSTEM |
| 3. Upstream Formulation | What did the formulation erase before it became clean? | DELETED_CARRIER |
| 4. Transfer Integrity T(M,S,R,C,N,B) | Did the receiver inherit the structure, or only the label? | TRANSFER_FAILURE |
| 5. Constraint Budget | Who pays the bill, and can the receiver survive it? | HIDDEN_BILL |

## Twelve Master Failure Signatures

| # | Signature | Core failure |
|---|-----------|-------------|
| 1 | False Closure | Claim closes before load-bearing condition is tested |
| 2 | Possible-Once → System-Admissible | One-off success becomes system claim |
| 3 | Deleted Carrier / Ghost Gradient | Output modeled without substrate |
| 4 | Transfer Failure | Label transfers; constraint state does not |
| 5 | Hidden Bill | Cost is spent but not declared |
| 6 | Static Fantasy | Time, drift, decay, and maintenance ignored |
| 7 | Representation Reified | Model, metric, or checklist treated as reality |
| 8 | Evidence-State Inflation | Weak support promoted to closure |
| 9 | Boundary Smuggling | Bounded result presented as universal |
| 10 | Receiver Collapse | Receiver capacity assumed |
| 11 | Governance Theater | Artifact treated as control |
| 12 | Behavior from Formal State | Rule or training treated as demonstrated behavior |

## Directive States

| State | Meaning |
|-------|---------|
| **ADVANCE** | Structurally allowed to continue under stated constraints |
| **REPAIR** | Missing carrier, budget, boundary, or transfer path |
| **HOLD** | Not enough information to judge |
| **BLOCK** | Structurally inadmissible under current framing |

## Quick Start

```python
from first_principles_audit import AuditInput, run_audit

result = run_audit(AuditInput(
    object_name="AI output pipeline",
    claim="Outputs are deployment-ready",
    domain="software",
    cost_declared=False,
    maintenance_declared=False,
    execution_demonstrated=False,
))
result.print_receipt()
# DIRECTIVE: REPAIR  (hidden bill + behavior from formal state)
```

## From Dict

```python
from first_principles_audit import audit_from_dict

result = audit_from_dict({
    "object_name": "governance policy",
    "claim": "Installing the policy will change behavior",
    "domain": "institutional",
    "carrier_declared": False,
    "governance_verified_behavior": False,
})
# DIRECTIVE: BLOCK
```

## Running Tests

```bash
python test_first_principles_audit.py
```

42 tests covering all five layers, all twelve failure signatures, all four directive states, and the twelve classic diagnostic phrases.

## Fifteen Core Diagnostic Phrases

1. The label survived, but the structure died.
2. Topic transfer is not constraint-state transfer.
3. Possible once is not system-admissible.
4. Utility is not proof.
5. Precision without correction is unpaid constraint debt.
6. A signal is not control unless it can trigger action.
7. A right without remedy is only a label.
8. Safety margin is not free capacity.
9. A plan is not execution.
10. The receiver inherits a ghost when the carrier is missing.
11. A model is not the system.
12. Training is not competence until performance is demonstrated.
13. Documentation is not knowledge transfer until the receiver can reconstruct and act.
14. A forecast is not capacity.
15. Compliance is not governance unless it can detect, halt, correct, and enforce.

## Claim Boundary

The framework outputs structural admissibility status — not truth claims. Output is always:

> "This claim is structurally admissible, repairable, held, or blocked under stated constraints."

Never: "This claim is true."

---
Engineering audit tool. No legal, medical, or domain authority.
