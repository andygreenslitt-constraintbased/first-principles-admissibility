"""
Tests for the First-Principles Admissibility Audit Engine.

Covers:
  - Clean input produces ADVANCE
  - Each layer in isolation produces the right failure signature
  - Directive resolution: ADVANCE / REPAIR / HOLD / BLOCK
  - Dominant signature is correct
  - audit_from_dict round-trip
  - to_dict has required keys
  - Missing required dict keys raise ValueError
  - AuditInput validation rejects out-of-range floats
"""

import sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from first_principles_audit import (
    AuditInput,
    AuditReceipt,
    Directive,
    FailureSignature,
    audit_from_dict,
    run_audit,
)


# ===========================================================================
# Helpers
# ===========================================================================

def _clean(**kwargs) -> AuditInput:
    """Fully-admissible base input with all defaults."""
    return AuditInput(object_name="obj", claim="claim", domain="test", **kwargs)


# ===========================================================================
# ADVANCE cases
# ===========================================================================

def test_all_defaults_advance():
    r = run_audit(_clean())
    assert r.directive == Directive.ADVANCE
    assert len(r.failed_layers) == 0


def test_advance_with_high_evidence():
    r = run_audit(_clean(evidence_strength=1.0))
    assert r.directive == Directive.ADVANCE


# ===========================================================================
# Layer 1 — False Closure
# ===========================================================================

def test_layer1_load_bearing_not_tested_fails():
    r = run_audit(_clean(load_bearing_condition_tested=False))
    assert r.directive == Directive.BLOCK
    assert FailureSignature.FALSE_CLOSURE in r.all_signatures


def test_layer1_closure_fluency_only_fails():
    r = run_audit(_clean(closure_based_on_fluency_only=True))
    assert r.directive == Directive.BLOCK
    assert FailureSignature.FALSE_CLOSURE in r.all_signatures


# ===========================================================================
# Layer 2 — First-Principles Admissibility
# ===========================================================================

def test_layer2_based_on_single_instance():
    r = run_audit(_clean(based_on_single_instance=True))
    assert FailureSignature.POSSIBLE_ONCE_SYSTEM in r.all_signatures
    assert r.directive in (Directive.REPAIR, Directive.BLOCK)


def test_layer2_not_scalable():
    r = run_audit(_clean(scalable=False))
    assert FailureSignature.POSSIBLE_ONCE_SYSTEM in r.all_signatures


def test_layer2_no_transfer_mechanism():
    r = run_audit(_clean(transfer_mechanism_declared=False))
    assert FailureSignature.DELETED_CARRIER in r.all_signatures
    assert r.directive == Directive.BLOCK


def test_layer2_no_decay_control():
    r = run_audit(_clean(decay_control_declared=False))
    assert FailureSignature.STATIC_FANTASY in r.all_signatures


# ===========================================================================
# Layer 3 — Upstream Formulation
# ===========================================================================

def test_layer3_carrier_not_declared_blocks():
    r = run_audit(_clean(carrier_declared=False))
    assert r.directive == Directive.BLOCK
    assert r.missing_carrier is True


def test_layer3_hidden_variables():
    r = run_audit(_clean(hidden_variables_declared=False))
    assert FailureSignature.DELETED_CARRIER in r.all_signatures


def test_layer3_corrections_not_declared():
    r = run_audit(_clean(corrections_declared=False))
    assert FailureSignature.HIDDEN_BILL in r.all_signatures


def test_layer3_utility_as_proof():
    r = run_audit(_clean(utility_not_used_as_proof=False))
    assert FailureSignature.EVIDENCE_STATE_INFLATION in r.all_signatures


def test_layer3_model_treated_as_system():
    r = run_audit(_clean(model_not_treated_as_system=False))
    assert FailureSignature.REPRESENTATION_REIFIED in r.all_signatures


# ===========================================================================
# Layer 4 — Transfer Integrity
# ===========================================================================

def test_layer4_only_label_transferred():
    r = run_audit(_clean(structure_transferred_not_label=False))
    assert FailureSignature.TRANSFER_FAILURE in r.all_signatures
    assert r.directive == Directive.REPAIR


def test_layer4_low_constraint_clarity():
    r = run_audit(_clean(constraint_clarity=0.2))
    assert FailureSignature.TRANSFER_FAILURE in r.all_signatures


def test_layer4_high_noise():
    r = run_audit(_clean(transfer_noise=0.8))
    assert FailureSignature.TRANSFER_FAILURE in r.all_signatures


def test_layer4_receiver_collapse():
    r = run_audit(_clean(receiver_state_confirmed=False))
    assert FailureSignature.RECEIVER_COLLAPSE in r.all_signatures


def test_layer4_boundary_smuggling():
    r = run_audit(_clean(result_scope_bounded=False))
    assert FailureSignature.BOUNDARY_SMUGGLING in r.all_signatures


# ===========================================================================
# Layer 5 — Constraint Budget
# ===========================================================================

def test_layer5_cost_not_declared():
    r = run_audit(_clean(cost_declared=False))
    assert r.hidden_bill is True
    assert FailureSignature.HIDDEN_BILL in r.all_signatures


def test_layer5_receiver_cannot_sustain():
    r = run_audit(_clean(receiver_can_sustain=False))
    assert FailureSignature.RECEIVER_COLLAPSE in r.all_signatures


def test_layer5_maintenance_not_declared():
    r = run_audit(_clean(maintenance_declared=False))
    assert FailureSignature.STATIC_FANTASY in r.all_signatures


def test_layer5_low_evidence():
    r = run_audit(_clean(evidence_strength=0.1))
    assert FailureSignature.EVIDENCE_STATE_INFLATION in r.all_signatures


def test_layer5_governance_theater():
    r = run_audit(_clean(governance_verified_behavior=False))
    assert FailureSignature.GOVERNANCE_THEATER in r.all_signatures


def test_layer5_behavior_from_formal_state():
    r = run_audit(_clean(execution_demonstrated=False))
    assert FailureSignature.BEHAVIOR_FROM_FORMAL_STATE in r.all_signatures


# ===========================================================================
# Directive resolution
# ===========================================================================

def test_deleted_carrier_always_blocks():
    r = run_audit(_clean(carrier_declared=False, transfer_mechanism_declared=False))
    assert r.directive == Directive.BLOCK


def test_hold_on_weak_evidence_only():
    r = run_audit(_clean(evidence_strength=0.2))
    # Evidence inflation alone goes to HOLD
    assert r.directive in (Directive.HOLD, Directive.REPAIR)


def test_repair_on_hidden_bill():
    r = run_audit(_clean(cost_declared=False))
    assert r.directive == Directive.REPAIR


# ===========================================================================
# Dominant signature
# ===========================================================================

def test_dominant_signature_is_first_triggered():
    r = run_audit(_clean(load_bearing_condition_tested=False))
    assert r.dominant_signature == FailureSignature.FALSE_CLOSURE


def test_advance_has_no_dominant_signature():
    r = run_audit(_clean())
    assert r.dominant_signature is None


# ===========================================================================
# to_dict
# ===========================================================================

def test_to_dict_has_required_keys():
    r = run_audit(_clean())
    d = r.to_dict()
    for key in ("object", "claim", "domain", "directive", "failed_layers",
                "missing_carrier", "hidden_bill", "binding_constraint",
                "dominant_signature", "all_signatures", "layer_detail"):
        assert key in d, f"Missing key: {key}"


# ===========================================================================
# audit_from_dict
# ===========================================================================

def test_audit_from_dict_basic():
    r = audit_from_dict({"object_name": "x", "claim": "y", "domain": "z"})
    assert r.directive == Directive.ADVANCE


def test_audit_from_dict_missing_required_raises():
    try:
        audit_from_dict({"claim": "y", "domain": "z"})
        assert False, "Should have raised"
    except ValueError:
        pass


def test_audit_from_dict_unknown_keys_ignored():
    r = audit_from_dict({
        "object_name": "x", "claim": "y", "domain": "z",
        "completely_unknown_key": "garbage",
    })
    assert r.directive == Directive.ADVANCE


def test_audit_from_dict_with_failure():
    r = audit_from_dict({
        "object_name": "policy",
        "claim": "this will change behavior",
        "domain": "institutional",
        "carrier_declared": False,
        "governance_verified_behavior": False,
    })
    assert r.directive == Directive.BLOCK


# ===========================================================================
# AuditInput validation
# ===========================================================================

def test_invalid_constraint_clarity_raises():
    try:
        inp = _clean(constraint_clarity=1.5)
        inp.validate()
        assert False, "Should have raised"
    except ValueError:
        pass


def test_invalid_transfer_noise_raises():
    try:
        inp = _clean(transfer_noise=-0.1)
        inp.validate()
        assert False, "Should have raised"
    except ValueError:
        pass


def test_invalid_evidence_strength_raises():
    try:
        inp = _clean(evidence_strength=2.0)
        inp.validate()
        assert False, "Should have raised"
    except ValueError:
        pass


# ===========================================================================
# Classic diagnostic phrase scenarios
# ===========================================================================

def test_label_survived_structure_died():
    # "The label survived, but the structure died."
    r = run_audit(_clean(
        structure_transferred_not_label=False,
        constraint_clarity=0.1,
    ))
    assert FailureSignature.TRANSFER_FAILURE in r.all_signatures


def test_possible_once_not_system_admissible():
    # "Possible once is not system-admissible."
    r = run_audit(_clean(
        based_on_single_instance=True,
        scalable=False,
    ))
    assert FailureSignature.POSSIBLE_ONCE_SYSTEM in r.all_signatures


def test_utility_is_not_proof():
    # "Utility is not proof."
    r = run_audit(_clean(utility_not_used_as_proof=False, evidence_strength=0.2))
    assert FailureSignature.EVIDENCE_STATE_INFLATION in r.all_signatures


def test_plan_is_not_execution():
    # "A plan is not execution."
    r = run_audit(_clean(execution_demonstrated=False))
    assert FailureSignature.BEHAVIOR_FROM_FORMAL_STATE in r.all_signatures


def test_compliance_is_not_governance():
    # "Compliance is not governance unless it can detect, halt, correct, and enforce."
    r = run_audit(_clean(governance_verified_behavior=False))
    assert FailureSignature.GOVERNANCE_THEATER in r.all_signatures


# ===========================================================================
# Runner
# ===========================================================================

if __name__ == "__main__":
    tests = [fn for name, fn in sorted(globals().items()) if name.startswith("test_")]
    passed = failed = 0
    for t in tests:
        try:
            t()
            print(f"  PASS  {t.__name__}")
            passed += 1
        except Exception as exc:
            print(f"  FAIL  {t.__name__}  —  {exc}")
            failed += 1
    print(f"\n{passed} passed, {failed} failed")
