#!/usr/bin/env python3
import argparse
import hashlib
import json
from pathlib import Path
import random

VERSION = "1.0"
SCHEMA_VERSION = "1.0.0"
PROFILE = "STOCRS-R-STRUCTURAL-RESOLUTION-1-D01"
RULEBOOK_ID = "STOCRS-R-RULEBOOK-1-D01"
OUTPUT_JSON = "STOCRS_R_Demo_v1_0.json"
OUTPUT_VERIFY = "STOCRS_R_Demo_v1_0_VERIFY.txt"


def stable_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"), ensure_ascii=False)


def hash_obj(obj):
    return hashlib.sha256(stable_json(obj).encode("utf-8")).hexdigest()


def input_node():
    return {
        "kind": "input",
        "deps": [],
        "rule_id": "DECLARED_INPUT",
        "params": {},
    }


def derived_node(deps, rule_id, params=None):
    return {
        "kind": "derived",
        "deps": list(deps),
        "rule_id": rule_id,
        "params": dict(params or {}),
    }


def build_base_program():
    return {
        "ITEM_A_PRICE": input_node(),
        "ITEM_B_PRICE": input_node(),
        "ITEM_A_QTY": input_node(),
        "ITEM_B_QTY": input_node(),
        "ITEM_A_TOTAL": derived_node(["ITEM_A_PRICE", "ITEM_A_QTY"], "MULTIPLY"),
        "ITEM_B_TOTAL": derived_node(["ITEM_B_PRICE", "ITEM_B_QTY"], "MULTIPLY"),
        "SUBTOTAL": derived_node(["ITEM_A_TOTAL", "ITEM_B_TOTAL"], "ADD"),
        "DISCOUNT": derived_node(
            ["SUBTOTAL"],
            "THRESHOLD_VALUE",
            {"threshold": 300, "value": 20},
        ),
        "AFTER_DISCOUNT": derived_node(["SUBTOTAL", "DISCOUNT"], "SUBTRACT"),
        "TAX": derived_node(
            ["AFTER_DISCOUNT"],
            "PERCENT_ROUND",
            {"rate": 0.10, "digits": 2},
        ),
        "SHIPPING": derived_node(
            ["AFTER_DISCOUNT"],
            "ZERO_IF_THRESHOLD_ELSE_VALUE",
            {"threshold": 300, "value": 30},
        ),
        "FINAL_TOTAL": derived_node(
            ["AFTER_DISCOUNT", "TAX", "SHIPPING"],
            "SUM_ROUND",
            {"digits": 2},
        ),
    }


def build_enhanced_program(coupon_amount):
    program = build_base_program()
    program["LOYALTY_COUPON"] = derived_node(
        ["AFTER_DISCOUNT"],
        "THRESHOLD_VALUE",
        {"threshold": 250, "value": coupon_amount},
    )
    program["AFTER_COUPON"] = derived_node(
        ["AFTER_DISCOUNT", "LOYALTY_COUPON"],
        "SUBTRACT",
    )
    program["TAX"] = derived_node(
        ["AFTER_COUPON"],
        "PERCENT_ROUND",
        {"rate": 0.10, "digits": 2},
    )
    program["FINAL_TOTAL"] = derived_node(
        ["AFTER_COUPON", "TAX", "SHIPPING"],
        "SUM_ROUND",
        {"digits": 2},
    )
    return program


def canonical_program(program):
    payload = {}
    for node in sorted(program):
        spec = program[node]
        payload[node] = {
            "kind": spec["kind"],
            "deps": list(spec["deps"]),
            "rule_id": spec["rule_id"],
            "params": spec["params"],
        }
    return payload


def program_identity(program):
    return hash_obj(
        {
            "profile": PROFILE,
            "schema_version": SCHEMA_VERSION,
            "rulebook_id": RULEBOOK_ID,
            "program": canonical_program(program),
        }
    )


def input_identity(inputs):
    return hash_obj({"declared_inputs": {k: inputs[k] for k in sorted(inputs)}})


def normalize_claims(claims):
    normalized = {}
    for node, raw in claims.items():
        values = raw if isinstance(raw, list) else [raw]
        unique = {}
        for value in values:
            unique[stable_json(value)] = value
        normalized[node] = [unique[key] for key in sorted(unique)]
    return normalized


def evidence_identity(claims):
    return hash_obj({"evidence": normalize_claims(claims)})


def apply_rule(spec, values):
    deps = spec["deps"]
    params = spec["params"]
    rule_id = spec["rule_id"]

    if rule_id == "MULTIPLY":
        result = 1
        for dep in deps:
            result *= values[dep]
        return result

    if rule_id == "ADD":
        return sum(values[dep] for dep in deps)

    if rule_id == "THRESHOLD_VALUE":
        return params["value"] if values[deps[0]] >= params["threshold"] else 0

    if rule_id == "SUBTRACT":
        return values[deps[0]] - values[deps[1]]

    if rule_id == "PERCENT_ROUND":
        return round(values[deps[0]] * params["rate"], int(params["digits"]))

    if rule_id == "ZERO_IF_THRESHOLD_ELSE_VALUE":
        return 0 if values[deps[0]] >= params["threshold"] else params["value"]

    if rule_id == "SUM_ROUND":
        return round(sum(values[dep] for dep in deps), int(params["digits"]))

    raise ValueError("Unknown rule_id: " + str(rule_id))


def resolve_supported_values(program, available_nodes, declared_inputs, presentation_order):
    available = set(available_nodes)
    values = {}
    unresolved = set()
    missing_inputs = set()
    frontiers = []

    for node in presentation_order:
        if node not in available or node not in program:
            continue
        spec = program[node]
        if spec["kind"] == "input":
            if node in declared_inputs:
                values[node] = declared_inputs[node]
            else:
                unresolved.add(node)
                missing_inputs.add(node)
        else:
            unresolved.add(node)

    while True:
        ready = []
        for node in unresolved:
            spec = program[node]
            if spec["kind"] != "derived":
                continue
            if all(dep in values for dep in spec["deps"]):
                ready.append(node)

        if not ready:
            break

        frontier = sorted(ready)
        for node in frontier:
            values[node] = apply_rule(program[node], values)
            unresolved.remove(node)
        frontiers.append(frontier)

    return values, unresolved, missing_inputs, frontiers


def descendants_of(program, roots):
    blocked = set(roots)
    changed = True
    while changed:
        changed = False
        for node, spec in program.items():
            if node in blocked:
                continue
            if any(dep in blocked for dep in spec["deps"]):
                blocked.add(node)
                changed = True
    return blocked


def resolve(
    program,
    declared_inputs,
    claims=None,
    available_nodes=None,
    presentation_order=None,
    target_node="FINAL_TOTAL",
):
    claims = claims or {}
    available_nodes = list(program.keys()) if available_nodes is None else list(available_nodes)
    presentation_order = list(available_nodes) if presentation_order is None else list(presentation_order)

    values, unresolved, missing_inputs, frontiers = resolve_supported_values(
        program=program,
        available_nodes=available_nodes,
        declared_inputs=declared_inputs,
        presentation_order=presentation_order,
    )

    normalized_claims = normalize_claims(claims)
    conflicts = {}

    for node in sorted(normalized_claims):
        claim_values = normalized_claims[node]

        if node not in program:
            conflicts[node] = {
                "type": "unknown_claim_node",
                "claims": claim_values,
            }
            continue

        if len(claim_values) > 1:
            conflicts[node] = {
                "type": "multi_value_conflict",
                "claims": claim_values,
            }
            continue

        if node not in values:
            conflicts[node] = {
                "type": "claim_without_supported_value",
                "claims": claim_values,
            }
            continue

        if stable_json(claim_values[0]) != stable_json(values[node]):
            conflicts[node] = {
                "type": "claim_vs_structure",
                "claim": claim_values[0],
                "supported_value": values[node],
            }

    blocked = descendants_of(program, conflicts.keys()) if conflicts else set()

    visible_values = {
        node: value
        for node, value in values.items()
        if node not in blocked
    }

    unresolved_final = set(unresolved)
    for node in blocked:
        if node in program and node not in conflicts:
            unresolved_final.add(node)

    if conflicts:
        state = "CONFLICT"
    elif unresolved_final:
        state = "INCOMPLETE"
    else:
        state = "RESOLVED"

    output_visible = state == "RESOLVED" and target_node in visible_values
    supported_output = visible_values.get(target_node) if output_visible else None

    semantic_payload = {
        "profile": PROFILE,
        "schema_version": SCHEMA_VERSION,
        "rulebook_id": RULEBOOK_ID,
        "program_identity": program_identity(program),
        "declared_input_identity": input_identity(declared_inputs),
        "evidence_identity": evidence_identity(claims),
        "available_nodes": sorted(node for node in available_nodes if node in program),
        "state": state,
        "output_visible": output_visible,
        "target_node": target_node,
        "supported_output": supported_output,
        "values": {k: visible_values[k] for k in sorted(visible_values)},
        "unresolved": sorted(unresolved_final),
        "missing_inputs": sorted(missing_inputs),
        "conflicts": conflicts,
        "blocked": sorted(blocked),
        "frontiers": frontiers,
    }

    result = dict(semantic_payload)
    result["certificate"] = hash_obj(semantic_payload)
    return result


def shuffled(items, seed):
    result = list(items)
    random.Random(seed).shuffle(result)
    return result


def run_demo(seed):
    base_program = build_base_program()
    enhanced_program_v1 = build_enhanced_program(15)
    enhanced_program_v2 = build_enhanced_program(25)

    base_inputs = {
        "ITEM_A_PRICE": 120,
        "ITEM_B_PRICE": 80,
        "ITEM_A_QTY": 2,
        "ITEM_B_QTY": 1,
    }

    second_inputs = {
        "ITEM_A_PRICE": 120,
        "ITEM_B_PRICE": 80,
        "ITEM_A_QTY": 1,
        "ITEM_B_QTY": 3,
    }

    base_nodes = list(base_program.keys())
    enhanced_nodes_v1 = list(enhanced_program_v1.keys())
    enhanced_nodes_v2 = list(enhanced_program_v2.keys())

    run_a = resolve(
        base_program,
        base_inputs,
        presentation_order=shuffled(base_nodes, seed),
    )
    run_b = resolve(
        base_program,
        base_inputs,
        presentation_order=shuffled(base_nodes, seed + 999),
    )

    reusable_template_run = resolve(
        base_program,
        second_inputs,
        presentation_order=shuffled(base_nodes, seed + 123),
    )

    incomplete_inputs = dict(base_inputs)
    incomplete_inputs.pop("ITEM_B_PRICE")
    incomplete_run = resolve(
        base_program,
        incomplete_inputs,
        presentation_order=shuffled(base_nodes, seed + 321),
    )

    compatible_claim_run = resolve(
        base_program,
        base_inputs,
        claims={"ITEM_A_PRICE": [120, 120]},
        presentation_order=shuffled(base_nodes, seed + 400),
    )

    multi_value_conflict_run = resolve(
        base_program,
        base_inputs,
        claims={"ITEM_A_PRICE": [120, 999]},
        presentation_order=shuffled(base_nodes, seed + 401),
    )

    unanimous_wrong_claim_run = resolve(
        base_program,
        base_inputs,
        claims={"ITEM_A_PRICE": [999, 999]},
        presentation_order=shuffled(base_nodes, seed + 402),
    )

    reverse_majority_claim_run = resolve(
        base_program,
        base_inputs,
        claims={"ITEM_A_PRICE": [999, 999, 120]},
        presentation_order=shuffled(base_nodes, seed + 403),
    )

    derived_wrong_claim_run = resolve(
        base_program,
        base_inputs,
        claims={"FINAL_TOTAL": 999},
        presentation_order=shuffled(base_nodes, seed + 404),
    )

    enhanced_run_v1 = resolve(
        enhanced_program_v1,
        base_inputs,
        presentation_order=shuffled(enhanced_nodes_v1, seed + 2026),
    )

    enhanced_run_v2 = resolve(
        enhanced_program_v2,
        base_inputs,
        presentation_order=shuffled(enhanced_nodes_v2, seed + 2027),
    )

    checks = {
        "same_program_same_inputs_same_output": run_a["supported_output"] == run_b["supported_output"],
        "same_program_same_inputs_same_state": run_a["state"] == run_b["state"],
        "same_program_same_inputs_same_certificate": run_a["certificate"] == run_b["certificate"],
        "same_program_identity_under_reordered_presentation": run_a["program_identity"] == run_b["program_identity"],
        "different_inputs_change_input_identity": run_a["declared_input_identity"] != reusable_template_run["declared_input_identity"],
        "incomplete_input_stays_incomplete": incomplete_run["state"] == "INCOMPLETE",
        "compatible_repeated_claim_resolves": compatible_claim_run["state"] == "RESOLVED",
        "multi_value_claim_conflicts": multi_value_conflict_run["state"] == "CONFLICT",
        "unanimous_wrong_claim_rejected": unanimous_wrong_claim_run["conflicts"].get("ITEM_A_PRICE", {}).get("type") == "claim_vs_structure",
        "reverse_majority_cannot_override": reverse_majority_claim_run["conflicts"].get("ITEM_A_PRICE", {}).get("type") == "multi_value_conflict",
        "wrong_derived_claim_rejected": derived_wrong_claim_run["conflicts"].get("FINAL_TOTAL", {}).get("type") == "claim_vs_structure",
        "enhancement_v1_program_identity_differs_from_base": enhanced_run_v1["program_identity"] != run_a["program_identity"],
        "policy_update_changes_program_identity": enhanced_run_v1["program_identity"] != enhanced_run_v2["program_identity"],
        "enhancement_v1_resolves": enhanced_run_v1["state"] == "RESOLVED",
        "enhancement_v2_resolves": enhanced_run_v2["state"] == "RESOLVED",
    }

    result = {
        "name": "STOCRS-R Reference Demonstration",
        "version": VERSION,
        "schema_version": SCHEMA_VERSION,
        "profile": PROFILE,
        "rulebook_id": RULEBOOK_ID,
        "principles": [
            "same complete program identity + same declared inputs -> same supported values",
            "same semantic resolution inputs -> same state + same certificate",
            "claim multiplicity != structural authority",
            "declared rule mutation -> new program identity -> deterministic new supported output",
        ],
        "base_program_identity": program_identity(base_program),
        "enhanced_program_v1_identity": program_identity(enhanced_program_v1),
        "enhanced_program_v2_identity": program_identity(enhanced_program_v2),
        "base_run_a": run_a,
        "base_run_b": run_b,
        "reusable_template_run": reusable_template_run,
        "incomplete_run": incomplete_run,
        "compatible_claim_run": compatible_claim_run,
        "multi_value_conflict_run": multi_value_conflict_run,
        "unanimous_wrong_claim_run": unanimous_wrong_claim_run,
        "reverse_majority_claim_run": reverse_majority_claim_run,
        "derived_wrong_claim_run": derived_wrong_claim_run,
        "enhanced_coupon_run_v1": enhanced_run_v1,
        "enhanced_coupon_run_v2": enhanced_run_v2,
        "base_final_total": run_a["supported_output"],
        "reused_template_final_total": reusable_template_run["supported_output"],
        "enhanced_final_total_v1": enhanced_run_v1["supported_output"],
        "enhanced_final_total_v2": enhanced_run_v2["supported_output"],
        "policy_update_story": "The coupon policy parameter changed from 15 to 25. The rulebook and resolver remained fixed, while program identity changed.",
        "checks": checks,
        "all_checks_pass": all(checks.values()),
    }

    result["demo_certificate"] = hash_obj(
        {
            "name": result["name"],
            "version": result["version"],
            "schema_version": result["schema_version"],
            "profile": result["profile"],
            "rulebook_id": result["rulebook_id"],
            "base_program_identity": result["base_program_identity"],
            "enhanced_program_v1_identity": result["enhanced_program_v1_identity"],
            "enhanced_program_v2_identity": result["enhanced_program_v2_identity"],
            "checks": result["checks"],
            "base_run_a_certificate": run_a["certificate"],
            "base_run_b_certificate": run_b["certificate"],
            "reusable_template_certificate": reusable_template_run["certificate"],
            "incomplete_certificate": incomplete_run["certificate"],
            "compatible_claim_certificate": compatible_claim_run["certificate"],
            "multi_value_conflict_certificate": multi_value_conflict_run["certificate"],
            "unanimous_wrong_claim_certificate": unanimous_wrong_claim_run["certificate"],
            "reverse_majority_claim_certificate": reverse_majority_claim_run["certificate"],
            "derived_wrong_claim_certificate": derived_wrong_claim_run["certificate"],
            "enhanced_v1_certificate": enhanced_run_v1["certificate"],
            "enhanced_v2_certificate": enhanced_run_v2["certificate"],
        }
    )

    return result


def write_outputs(result):
    repo_root = Path(__file__).resolve().parent.parent
    outputs_dir = repo_root / "outputs"
    outputs_dir.mkdir(parents=True, exist_ok=True)

    json_path = outputs_dir / OUTPUT_JSON
    verify_path = outputs_dir / OUTPUT_VERIFY

    with json_path.open("w", encoding="utf-8") as handle:
        json.dump(result, handle, indent=2, sort_keys=True, ensure_ascii=False)
        handle.write("\n")

    with verify_path.open("w", encoding="utf-8") as handle:
        handle.write("STOCRS-R Reference Demonstration v1.0 VERIFY\n")
        handle.write("Profile: " + PROFILE + "\n")
        handle.write("Schema: " + SCHEMA_VERSION + "\n")
        handle.write("Rulebook: " + RULEBOOK_ID + "\n\n")
        handle.write("Base final total: " + str(result["base_final_total"]) + "\n")
        handle.write("Reused template final total: " + str(result["reused_template_final_total"]) + "\n")
        handle.write("Enhanced final total v1: " + str(result["enhanced_final_total_v1"]) + "\n")
        handle.write("Enhanced final total v2: " + str(result["enhanced_final_total_v2"]) + "\n\n")
        handle.write("Base program identity: " + result["base_program_identity"] + "\n")
        handle.write("Enhanced program v1 identity: " + result["enhanced_program_v1_identity"] + "\n")
        handle.write("Enhanced program v2 identity: " + result["enhanced_program_v2_identity"] + "\n\n")
        for name, passed in result["checks"].items():
            handle.write(name + ": " + ("PASS" if passed else "FAIL") + "\n")
        handle.write("\nALL CHECKS: " + ("PASS" if result["all_checks_pass"] else "FAIL") + "\n")
        handle.write("Demo certificate: " + result["demo_certificate"] + "\n")

    return json_path, verify_path


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=101)
    parser.add_argument("--no-write", action="store_true")
    args = parser.parse_args()

    result = run_demo(args.seed)

    print("STOCRS-R Reference Demonstration v1.0")
    print()
    print("Base final total:", result["base_final_total"])
    print("Reused template final total:", result["reused_template_final_total"])
    print("Enhanced final total v1:", result["enhanced_final_total_v1"])
    print("Enhanced final total v2:", result["enhanced_final_total_v2"])
    print()
    for name, passed in result["checks"].items():
        print(name + ":", "PASS" if passed else "FAIL")
    print()
    print("ALL CHECKS:", "PASS" if result["all_checks_pass"] else "FAIL")
    print("Demo certificate:", result["demo_certificate"])

    if not args.no_write:
        json_path, verify_path = write_outputs(result)
        print("Created:", json_path)
        print("Created:", verify_path)


if __name__ == "__main__":
    main()
