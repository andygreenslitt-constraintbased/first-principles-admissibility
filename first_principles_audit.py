"""
First-Principles Admissibility Framework — Audit Engine

A structural claim auditor.

Does not ask: "Does this sound right?"
Asks: "What breaks first, and was that break declared before movement?"

Core rule:
    Possible != Repeatable != Scalable != Transferable != Admissible

Five audit layers:
    1. False Closure
    2. First-Principles Admissibility  F(X) = {P, S, T, D}
    3. Upstream Formulation Failure
    4. Transfer Integrity             T(M, S, R, C, N, B)
    5. Constraint Budget

Output: ADVANCE | REPAIR | HOLD | BLOCK

Engineering audit tool only. Not a legal, medical, or safety authority.
"""

from __future__ import annotations

from dataclasses import dataclass, field, asdict
from enum import Enum
from typing import List, Optional, Tuple


# ---------------------------------------------------------------------------
# Directive states
# ---------------------------------------------------------------------------

class Directive(str, Enum):
    ADVANCE = "ADVANCE"   # structurally allowed to continue under stated constraints
    REPAIR  = "REPAIR"    # missing carrier, budget, boundary, transfer path, evidence state, or correction loop
    HOLD    = "HOLD"      # not enough information to judge
    BLOCK   = "BLOCK"     # structurally inadmissible under current framing


# ---------------------------------------------------------------------------
# The twelve master failure signatures
# ---------------------------------------------------------------------------

class FailureSignature(str, Enum):
    FALSE_CLOSURE              = "false_closure"
    POSSIBLE_ONCE_SYSTEM       = "possible_once_system_admissible"
    DELETED_CARRIER            = "deleted_carrier_ghost_gradient"
    TRANSFER_FAILURE           = "transfer_failure"
    HIDDEN_BILL                = "hidden_bill"
    STATIC_FANTASY             = "static_fantasy"
    REPRESENTATION_REIFIED     = "representation_reified"
    EVIDENCE_STATE_INFLATION   = "evidence_state_inflation"
    BOUNDARY_SMUGGLING         = "boundary_smuggling"
    RECEIVER_COLLAPSE          = "receiver_collapse"
    GOVERNANCE_THEATER         = "governance_theater"
    BEHAVIOR_FROM_FORMAL_STATE = "behavior_from_formal_state"

    # Human-readable labels
    @property
    def label(self) -> str:
        return {
            "false_closure":                     "False Closure",
            "possible_once_system_admissible":   "Possible-Once -> System-Admissible",
            "deleted_carrier_ghost_gradient":    "Deleted Carrier / Ghost Gradient",
            "transfer_failure":                  "Transfer Failure",
            "hidden_bill":                       "Hidden Bill",
            "static_fantasy":                    "Static Fantasy",
            "representation_reified":            "Representation Reified",
            "evidence_state_inflation":          "Evidence-State Inflation",
            "boundary_smuggling":                "Boundary Smuggling",
            "receiver_collapse":                 "Receiver Collapse",
            "governance_theater":                "Governance Theater",
            "behavior_from_formal_state":        "Behavior from Formal State",
        }[self.value]


# ---------------------------------------------------------------------------
# Audit input
# ---------------------------------------------------------------------------

@dataclass
class AuditInput:
    """
    Full input surface for the five-layer audit.

    Required:
        object_name — what is being audited
        claim       — the specific claim being assessed
        domain      — context domain

    Layer fields default to the most favorable value. Set any to False/low
    to trigger the corresponding failure signature.
    """

    # ---- Identity ----
    object_name: str
    claim: str
    domain: str

    # ---- Layer 1: False Closure ----
    # Did the claim close before the load-bearing condition was tested?
    load_bearing_condition_tested: bool = True
    # Is the apparent completeness based only on fluent presentation, consensus, or authority?
    closure_based_on_fluency_only: bool = False

    # ---- Layer 2: First-Principles Admissibility F(X) = {P, S, T, D} ----
    # P — physical/logical possibility confirmed
    possibility_confirmed: bool = True
    # S — survives scale and repetition
    scalable: bool = True
    # T — transfer mechanism declared
    transfer_mechanism_declared: bool = True
    # D — decay/drift control declared
    decay_control_declared: bool = True

    # ---- Layer 3: Upstream Formulation ----
    # Carrier declared (output substrate is present)
    carrier_declared: bool = True
    # Hidden variables declared (nothing erased before the math began)
    hidden_variables_declared: bool = True
    # Unpaid corrections declared
    corrections_declared: bool = True
    # No utility-as-proof substitution
    utility_not_used_as_proof: bool = True

    # ---- Layer 4: Transfer Integrity T(M, S, R, C, N, B) ----
    # M — carried object is the structure (not only the label)
    structure_transferred_not_label: bool = True
    # C — constraint clarity: 0.0 (none) to 1.0 (fully declared)
    constraint_clarity: float = 1.0
    # N — noise / distortion: 0.0 (none) to 1.0 (fully corrupted)
    transfer_noise: float = 0.0
    # B — preservation budget declared
    preservation_budget_declared: bool = True
    # Receiver state confirmed capable
    receiver_state_confirmed: bool = True

    # ---- Layer 5: Constraint Budget ----
    # Cost declared
    cost_declared: bool = True
    # Receiver can sustain the bill
    receiver_can_sustain: bool = True
    # Maintenance declared
    maintenance_declared: bool = True
    # Safety margin is not presented as free capacity
    safety_margin_not_free: bool = True

    # ---- Context flags ----
    # "works-once" flag — claim based on a single instance
    based_on_single_instance: bool = False
    # Decay/time/drift is acknowledged
    time_decay_acknowledged: bool = True
    # The model/metric is not being treated as the system itself
    model_not_treated_as_system: bool = True
    # Evidence strength: 0.0 (anecdote) to 1.0 (fully tested)
    evidence_strength: float = 1.0
    # Result scope: True = bounded, False = being presented as universal
    result_scope_bounded: bool = True
    # Governance is verified behavior, not just artifact
    governance_verified_behavior: bool = True
    # Plans/instructions accompanied by demonstrated execution
    execution_demonstrated: bool = True

    def validate(self) -> None:
        if not 0.0 <= self.constraint_clarity <= 1.0:
            raise ValueError("constraint_clarity must be in [0, 1]")
        if not 0.0 <= self.transfer_noise <= 1.0:
            raise ValueError("transfer_noise must be in [0, 1]")
        if not 0.0 <= self.evidence_strength <= 1.0:
            raise ValueError("evidence_strength must be in [0, 1]")


# ---------------------------------------------------------------------------
# Layer evaluators
# ---------------------------------------------------------------------------

def _layer1_false_closure(inp: AuditInput) -> Tuple[bool, List[FailureSignature]]:
    sigs: List[FailureSignature] = []
    passed = True
    if not inp.load_bearing_condition_tested:
        sigs.append(FailureSignature.FALSE_CLOSURE)
        passed = False
    if inp.closure_based_on_fluency_only:
        sigs.append(FailureSignature.FALSE_CLOSURE)
        passed = False
    return passed, sigs


def _layer2_first_principles(inp: AuditInput) -> Tuple[bool, List[FailureSignature]]:
    sigs: List[FailureSignature] = []
    passed = True
    if inp.based_on_single_instance:
        sigs.append(FailureSignature.POSSIBLE_ONCE_SYSTEM)
        passed = False
    if not inp.possibility_confirmed:
        sigs.append(FailureSignature.FALSE_CLOSURE)
        passed = False
    if not inp.scalable:
        sigs.append(FailureSignature.POSSIBLE_ONCE_SYSTEM)
        passed = False
    if not inp.transfer_mechanism_declared:
        sigs.append(FailureSignature.DELETED_CARRIER)
        passed = False
    if not inp.decay_control_declared:
        sigs.append(FailureSignature.STATIC_FANTASY)
        passed = False
    return passed, sigs


def _layer3_upstream(inp: AuditInput) -> Tuple[bool, List[FailureSignature]]:
    sigs: List[FailureSignature] = []
    passed = True
    if not inp.carrier_declared:
        sigs.append(FailureSignature.DELETED_CARRIER)
        passed = False
    if not inp.hidden_variables_declared:
        sigs.append(FailureSignature.DELETED_CARRIER)
        passed = False
    if not inp.corrections_declared:
        sigs.append(FailureSignature.HIDDEN_BILL)
        passed = False
    if not inp.utility_not_used_as_proof:
        sigs.append(FailureSignature.EVIDENCE_STATE_INFLATION)
        passed = False
    if not inp.model_not_treated_as_system:
        sigs.append(FailureSignature.REPRESENTATION_REIFIED)
        passed = False
    return passed, sigs


def _layer4_transfer(inp: AuditInput) -> Tuple[bool, List[FailureSignature]]:
    sigs: List[FailureSignature] = []
    passed = True
    if not inp.structure_transferred_not_label:
        sigs.append(FailureSignature.TRANSFER_FAILURE)
        passed = False
    if inp.constraint_clarity < 0.5:
        sigs.append(FailureSignature.TRANSFER_FAILURE)
        passed = False
    if inp.transfer_noise > 0.5:
        sigs.append(FailureSignature.TRANSFER_FAILURE)
        passed = False
    if not inp.preservation_budget_declared:
        sigs.append(FailureSignature.HIDDEN_BILL)
        passed = False
    if not inp.receiver_state_confirmed:
        sigs.append(FailureSignature.RECEIVER_COLLAPSE)
        passed = False
    if not inp.result_scope_bounded:
        sigs.append(FailureSignature.BOUNDARY_SMUGGLING)
        passed = False
    return passed, sigs


def _layer5_budget(inp: AuditInput) -> Tuple[bool, List[FailureSignature]]:
    sigs: List[FailureSignature] = []
    passed = True
    if not inp.cost_declared:
        sigs.append(FailureSignature.HIDDEN_BILL)
        passed = False
    if not inp.receiver_can_sustain:
        sigs.append(FailureSignature.RECEIVER_COLLAPSE)
        passed = False
    if not inp.maintenance_declared:
        sigs.append(FailureSignature.STATIC_FANTASY)
        passed = False
    if not inp.safety_margin_not_free:
        sigs.append(FailureSignature.HIDDEN_BILL)
        passed = False
    if not inp.time_decay_acknowledged:
        sigs.append(FailureSignature.STATIC_FANTASY)
        passed = False
    if inp.evidence_strength < 0.3:
        sigs.append(FailureSignature.EVIDENCE_STATE_INFLATION)
        passed = False
    if not inp.governance_verified_behavior:
        sigs.append(FailureSignature.GOVERNANCE_THEATER)
        passed = False
    if not inp.execution_demonstrated:
        sigs.append(FailureSignature.BEHAVIOR_FROM_FORMAL_STATE)
        passed = False
    return passed, sigs


# ---------------------------------------------------------------------------
# Directive resolver
# ---------------------------------------------------------------------------

LAYER_NAMES = [
    "false_closure",
    "first_principles_admissibility",
    "upstream_formulation",
    "transfer_integrity",
    "constraint_budget",
]


def _resolve_directive(
    layer_passes: List[bool],
    all_signatures: List[FailureSignature],
) -> Directive:
    failed_count = sum(1 for p in layer_passes if not p)
    if failed_count == 0:
        return Directive.ADVANCE
    if FailureSignature.FALSE_CLOSURE in all_signatures and not layer_passes[0]:
        # Layer 1 failure — hard block on false closure
        return Directive.BLOCK
    if FailureSignature.DELETED_CARRIER in all_signatures:
        return Directive.BLOCK
    if FailureSignature.TRANSFER_FAILURE in all_signatures:
        return Directive.REPAIR
    if FailureSignature.EVIDENCE_STATE_INFLATION in all_signatures:
        return Directive.HOLD
    if failed_count == 1:
        return Directive.REPAIR
    return Directive.BLOCK


# ---------------------------------------------------------------------------
# Audit result
# ---------------------------------------------------------------------------

@dataclass(frozen=True)
class LayerResult:
    layer: str
    passed: bool
    signatures: Tuple[FailureSignature, ...]


@dataclass
class AuditReceipt:
    """Structured audit output."""
    object_name: str
    claim: str
    domain: str

    layer_results: Tuple[LayerResult, ...]
    dominant_signature: Optional[FailureSignature]
    all_signatures: Tuple[FailureSignature, ...]
    failed_layers: Tuple[str, ...]
    directive: Directive

    missing_carrier: bool
    hidden_bill: bool
    binding_constraint: str

    def to_dict(self) -> dict:
        return {
            "object": self.object_name,
            "claim": self.claim,
            "domain": self.domain,
            "directive": self.directive.value,
            "dominant_signature": self.dominant_signature.label if self.dominant_signature else None,
            "all_signatures": [s.label for s in self.all_signatures],
            "failed_layers": list(self.failed_layers),
            "missing_carrier": self.missing_carrier,
            "hidden_bill": self.hidden_bill,
            "binding_constraint": self.binding_constraint,
            "layer_detail": [
                {
                    "layer": lr.layer,
                    "passed": lr.passed,
                    "signatures": [s.label for s in lr.signatures],
                }
                for lr in self.layer_results
            ],
        }

    def print_receipt(self) -> None:
        """Print the compressed audit receipt."""
        print("=" * 60)
        print("FIRST-PRINCIPLES ADMISSIBILITY AUDIT RECEIPT")
        print("=" * 60)
        print(f"Object:            {self.object_name}")
        print(f"Claim:             {self.claim}")
        print(f"Domain:            {self.domain}")
        print()
        print(f"Missing carrier:   {self.missing_carrier}")
        print(f"Hidden bill:       {self.hidden_bill}")
        print(f"Binding constraint:{self.binding_constraint}")
        print()
        if self.dominant_signature:
            print(f"Master signature:  {self.dominant_signature.label}")
        failed = ", ".join(self.failed_layers) if self.failed_layers else "none"
        print(f"Failed layer(s):   {failed}")
        print()
        print(f"DIRECTIVE:         {self.directive.value}")
        print("=" * 60)
        print("No-truth-claim: true")


# ---------------------------------------------------------------------------
# Main audit function
# ---------------------------------------------------------------------------

def run_audit(inp: AuditInput) -> AuditReceipt:
    """
    Run the five-layer first-principles admissibility audit.

    Returns an AuditReceipt with directive and structured findings.
    """
    inp.validate()

    evaluators = [
        (_layer1_false_closure,   LAYER_NAMES[0]),
        (_layer2_first_principles, LAYER_NAMES[1]),
        (_layer3_upstream,         LAYER_NAMES[2]),
        (_layer4_transfer,         LAYER_NAMES[3]),
        (_layer5_budget,           LAYER_NAMES[4]),
    ]

    layer_results: List[LayerResult] = []
    all_sigs: List[FailureSignature] = []
    layer_passes: List[bool] = []

    for fn, name in evaluators:
        passed, sigs = fn(inp)
        layer_results.append(LayerResult(layer=name, passed=passed, signatures=tuple(sigs)))
        all_sigs.extend(sigs)
        layer_passes.append(passed)

    failed_layers = tuple(
        lr.layer for lr in layer_results if not lr.passed
    )

    # Deduplicate signatures preserving order
    seen: set = set()
    unique_sigs: List[FailureSignature] = []
    for s in all_sigs:
        if s not in seen:
            unique_sigs.append(s)
            seen.add(s)

    dominant = unique_sigs[0] if unique_sigs else None
    directive = _resolve_directive(layer_passes, unique_sigs)

    missing_carrier = (
        FailureSignature.DELETED_CARRIER in unique_sigs
        or not inp.carrier_declared
    )
    hidden_bill = (
        FailureSignature.HIDDEN_BILL in unique_sigs
        or not inp.cost_declared
        or not inp.maintenance_declared
    )

    if failed_layers:
        binding = failed_layers[0]
    else:
        binding = "none"

    return AuditReceipt(
        object_name=inp.object_name,
        claim=inp.claim,
        domain=inp.domain,
        layer_results=tuple(layer_results),
        dominant_signature=dominant,
        all_signatures=tuple(unique_sigs),
        failed_layers=failed_layers,
        directive=directive,
        missing_carrier=missing_carrier,
        hidden_bill=hidden_bill,
        binding_constraint=binding,
    )


# ---------------------------------------------------------------------------
# Convenience: build from dict
# ---------------------------------------------------------------------------

def audit_from_dict(d: dict) -> AuditReceipt:
    """
    Build and run an audit from a plain dictionary.
    Required keys: object_name, claim, domain.
    All other keys map directly to AuditInput fields.
    """
    required = {"object_name", "claim", "domain"}
    missing = required - set(d.keys())
    if missing:
        raise ValueError(f"Missing required keys: {missing}")
    valid = {f for f in AuditInput.__dataclass_fields__}
    filtered = {k: v for k, v in d.items() if k in valid}
    return run_audit(AuditInput(**filtered))


# ---------------------------------------------------------------------------
# Built-in demo
# ---------------------------------------------------------------------------

def _demo() -> None:
    print("\n--- Demo 1: fully admissible claim ---")
    result = run_audit(AuditInput(
        object_name="Hydraulic leveling for pyramid base",
        claim="Still water surface establishes horizontal datum to sub-mm accuracy",
        domain="ancient_engineering",
    ))
    result.print_receipt()

    print("\n--- Demo 2: possible-once -> system claim (fails) ---")
    result2 = run_audit(AuditInput(
        object_name="One successful lift",
        claim="The system can reliably transport all 2.3 million blocks",
        domain="ancient_engineering",
        based_on_single_instance=True,
        scalable=False,
        decay_control_declared=False,
    ))
    result2.print_receipt()

    print("\n--- Demo 3: hidden bill (REPAIR) ---")
    result3 = run_audit(AuditInput(
        object_name="AI output pipeline",
        claim="Outputs are deployment-ready",
        domain="software",
        cost_declared=False,
        maintenance_declared=False,
        execution_demonstrated=False,
    ))
    result3.print_receipt()

    print("\n--- Demo 4: deleted carrier (BLOCK) ---")
    result4 = run_audit(AuditInput(
        object_name="Governance framework",
        claim="Installing the policy will change behavior",
        domain="institutional",
        carrier_declared=False,
        structure_transferred_not_label=False,
        governance_verified_behavior=False,
    ))
    result4.print_receipt()


if __name__ == "__main__":
    _demo()
