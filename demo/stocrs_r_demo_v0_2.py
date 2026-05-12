#!/usr/bin/env python3
import argparse
import hashlib
import json
import random
from copy import deepcopy

VERSION = "0.2"
OUT_VERIFY = "STOCRS_R_Demo_v0_2_VERIFY.txt"
OUT_JSON = "STOCRS_R_Demo_v0_2.json"


def stable_json(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def hash_obj(obj):
    return hashlib.sha256(stable_json(obj).encode("utf-8")).hexdigest()


def normalize_claims(claims):
    normalized = {}
    for node, value in claims.items():
        if isinstance(value, list):
            normalized[node] = list(value)
        else:
            normalized[node] = [value]
    return normalized


def resolve_claims(claims):
    accepted = {}
    conflicts = {}
    normalized = normalize_claims(claims)

    for node, values in normalized.items():
        unique = []
        seen = set()
        for value in values:
            key = stable_json(value)
            if key not in seen:
                seen.add(key)
                unique.append(value)

        if len(unique) == 1:
            accepted[node] = unique[0]
        else:
            conflicts[node] = {
                "type": "multi_value_conflict",
                "claims": unique,
            }

    return accepted, conflicts


def build_base_structure():
    return {
        "ITEM_A_PRICE": {"deps": [], "func": lambda v: 120},
        "ITEM_B_PRICE": {"deps": [], "func": lambda v: 80},
        "ITEM_A_QTY": {"deps": [], "func": lambda v: 2},
        "ITEM_B_QTY": {"deps": [], "func": lambda v: 1},
        "ITEM_A_TOTAL": {"deps": ["ITEM_A_PRICE", "ITEM_A_QTY"], "func": lambda v: v["ITEM_A_PRICE"] * v["ITEM_A_QTY"]},
        "ITEM_B_TOTAL": {"deps": ["ITEM_B_PRICE", "ITEM_B_QTY"], "func": lambda v: v["ITEM_B_PRICE"] * v["ITEM_B_QTY"]},
        "SUBTOTAL": {"deps": ["ITEM_A_TOTAL", "ITEM_B_TOTAL"], "func": lambda v: v["ITEM_A_TOTAL"] + v["ITEM_B_TOTAL"]},
        "DISCOUNT": {"deps": ["SUBTOTAL"], "func": lambda v: 20 if v["SUBTOTAL"] >= 300 else 0},
        "AFTER_DISCOUNT": {"deps": ["SUBTOTAL", "DISCOUNT"], "func": lambda v: v["SUBTOTAL"] - v["DISCOUNT"]},
        "TAX": {"deps": ["AFTER_DISCOUNT"], "func": lambda v: round(v["AFTER_DISCOUNT"] * 0.10, 2)},
        "SHIPPING": {"deps": ["AFTER_DISCOUNT"], "func": lambda v: 0 if v["AFTER_DISCOUNT"] >= 300 else 30},
        "FINAL_TOTAL": {"deps": ["AFTER_DISCOUNT", "TAX", "SHIPPING"], "func": lambda v: round(v["AFTER_DISCOUNT"] + v["TAX"] + v["SHIPPING"], 2)},
    }


def add_enhancement_coupon(program):
    upgraded = deepcopy(program)
    upgraded["LOYALTY_COUPON"] = {"deps": ["AFTER_DISCOUNT"], "func": lambda v: 15 if v["AFTER_DISCOUNT"] >= 250 else 0}
    upgraded["AFTER_COUPON"] = {"deps": ["AFTER_DISCOUNT", "LOYALTY_COUPON"], "func": lambda v: v["AFTER_DISCOUNT"] - v["LOYALTY_COUPON"]}
    upgraded["TAX"] = {"deps": ["AFTER_COUPON"], "func": lambda v: round(v["AFTER_COUPON"] * 0.10, 2)}
    upgraded["SHIPPING"] = {"deps": ["AFTER_DISCOUNT"], "func": lambda v: 0 if v["AFTER_DISCOUNT"] >= 300 else 30}
    upgraded["FINAL_TOTAL"] = {"deps": ["AFTER_COUPON", "TAX", "SHIPPING"], "func": lambda v: round(v["AFTER_COUPON"] + v["TAX"] + v["SHIPPING"], 2)}
    return upgraded


def structural_signature(program, known_nodes):
    payload = {}
    for node in sorted(known_nodes):
        if node in program:
            payload[node] = {
                "deps": list(program[node]["deps"]),
            }
    return hash_obj(payload)


def resolve(program, known_nodes, claims=None):
    claims = claims or {}
    accepted_claims, conflicts = resolve_claims(claims)

    values = {}
    frontiers = []
    unresolved = set()
    blocked = set(conflicts.keys())

    for node in known_nodes:
        if node in program:
            unresolved.add(node)

    for node, value in accepted_claims.items():
        if node in unresolved:
            values[node] = value
            unresolved.remove(node)

    while True:
        ready = []
        for node in unresolved:
            if node in blocked:
                continue
            deps = program[node]["deps"]
            if all(dep in values for dep in deps) and not any(dep in blocked for dep in deps):
                ready.append(node)

        if not ready:
            break

        frontier = sorted(ready)
        for node in frontier:
            values[node] = program[node]["func"](values)
            unresolved.remove(node)

        frontiers.append(frontier)

    changed = True
    while changed:
        changed = False
        for node in list(unresolved):
            deps = program[node]["deps"]
            if any(dep in blocked for dep in deps):
                blocked.add(node)
                unresolved.remove(node)
                changed = True

    state = "RESOLVED"
    if conflicts or blocked:
        state = "CONFLICT"
    elif unresolved:
        state = "INCOMPLETE"

    result = {
        "state": state,
        "known_nodes": sorted([node for node in known_nodes if node in program]),
        "known_count": len([node for node in known_nodes if node in program]),
        "values": values,
        "frontiers": frontiers,
        "unresolved": sorted(unresolved),
        "conflicts": conflicts,
        "blocked": sorted(blocked),
        "structure_signature": structural_signature(program, known_nodes),
    }
    result["certificate"] = hash_obj(result)
    return result


def shuffled(nodes, seed):
    data = list(nodes)
    rng = random.Random(seed)
    rng.shuffle(data)
    return data


def run_demo(seed):
    base_program = build_base_structure()
    base_nodes = list(base_program.keys())

    run_a = resolve(base_program, shuffled(base_nodes, seed))
    run_b = resolve(base_program, shuffled(base_nodes, seed + 999))

    reusable_order_structure = [
        "ITEM_A_PRICE",
        "ITEM_B_PRICE",
        "ITEM_A_QTY",
        "ITEM_B_QTY",
        "ITEM_A_TOTAL",
        "ITEM_B_TOTAL",
        "SUBTOTAL",
        "DISCOUNT",
        "AFTER_DISCOUNT",
        "TAX",
        "SHIPPING",
        "FINAL_TOTAL",
    ]

    second_order_claims = {
        "ITEM_A_PRICE": 120,
        "ITEM_B_PRICE": 80,
        "ITEM_A_QTY": 1,
        "ITEM_B_QTY": 3,
    }
    reused_template_run = resolve(base_program, reusable_order_structure, second_order_claims)

    incomplete_nodes = [
        "ITEM_A_PRICE",
        "ITEM_A_QTY",
        "ITEM_A_TOTAL",
        "ITEM_B_TOTAL",
        "SUBTOTAL",
        "DISCOUNT",
        "AFTER_DISCOUNT",
        "TAX",
        "SHIPPING",
        "FINAL_TOTAL",
    ]
    incomplete_run = resolve(base_program, incomplete_nodes)

    conflict_claims = {
        "ITEM_A_PRICE": [120, 999],
        "ITEM_B_PRICE": 80,
        "ITEM_A_QTY": 2,
        "ITEM_B_QTY": 1,
    }
    conflict_run = resolve(base_program, base_nodes, conflict_claims)

    enhanced_program = add_enhancement_coupon(base_program)
    enhanced_nodes = list(enhanced_program.keys())
    enhanced_run = resolve(enhanced_program, shuffled(enhanced_nodes, seed + 2026))

    base_total = run_a["values"].get("FINAL_TOTAL")
    enhanced_total = enhanced_run["values"].get("FINAL_TOTAL")

    output = {
        "name": "STOCRS-R Demo",
        "version": VERSION,
        "principle": "output = resolve(structure)",
        "law": "output_visible iff structure_complete AND structure_consistent",
        "classical_view": "execute steps in sequence to produce output",
        "stocrs_r_view": "resolve admissible structure to reveal output",
        "base_order_run_a": run_a,
        "base_order_run_b": run_b,
        "same_structure_same_output": run_a["values"].get("FINAL_TOTAL") == run_b["values"].get("FINAL_TOTAL"),
        "same_structure_same_state": run_a["state"] == run_b["state"],
        "same_structure_same_certificate": run_a["certificate"] == run_b["certificate"],
        "reusable_template_run": reused_template_run,
        "incomplete_run": incomplete_run,
        "conflict_run": conflict_run,
        "enhanced_coupon_run": enhanced_run,
        "base_final_total": base_total,
        "reused_template_final_total": reused_template_run["values"].get("FINAL_TOTAL"),
        "enhanced_final_total": enhanced_total,
        "enhancement_improves_total": enhanced_total < base_total,
        "enhancement_savings": round(base_total - enhanced_total, 2),
    }

    output["demo_certificate"] = hash_obj(output)
    return output


def write_outputs(result):
    with open(OUT_JSON, "w", encoding="utf-8") as f:
        json.dump(result, f, indent=2, sort_keys=True)

    with open(OUT_VERIFY, "w", encoding="utf-8") as f:
        f.write("STOCRS-R Demo v0.2 VERIFY\n")
        f.write("Output is resolved from structure.\n\n")
        f.write("Principle: output = resolve(structure)\n")
        f.write("Law: output_visible iff structure_complete AND structure_consistent\n\n")
        f.write("Classical view: execute steps in sequence to produce output\n")
        f.write("STOCRS-R view: resolve admissible structure to reveal output\n\n")
        f.write("Base final total: " + str(result["base_final_total"]) + "\n")
        f.write("Reused template final total: " + str(result["reused_template_final_total"]) + "\n")
        f.write("Enhanced final total: " + str(result["enhanced_final_total"]) + "\n")
        f.write("Enhancement improves total: " + str(result["enhancement_improves_total"]) + "\n")
        f.write("Enhancement savings: " + str(result["enhancement_savings"]) + "\n\n")
        f.write("Same structure same output: " + str(result["same_structure_same_output"]) + "\n")
        f.write("Same structure same state: " + str(result["same_structure_same_state"]) + "\n")
        f.write("Same structure same certificate: " + str(result["same_structure_same_certificate"]) + "\n")
        f.write("Incomplete state: " + result["incomplete_run"]["state"] + "\n")
        f.write("Conflict state: " + result["conflict_run"]["state"] + "\n\n")
        f.write("Base run A certificate: " + result["base_order_run_a"]["certificate"] + "\n")
        f.write("Base run B certificate: " + result["base_order_run_b"]["certificate"] + "\n")
        f.write("Reusable template certificate: " + result["reusable_template_run"]["certificate"] + "\n")
        f.write("Enhanced run certificate: " + result["enhanced_coupon_run"]["certificate"] + "\n")
        f.write("Demo certificate: " + result["demo_certificate"] + "\n")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--seed", type=int, default=101)
    args = parser.parse_args()

    result = run_demo(args.seed)
    write_outputs(result)

    print("STOCRS-R Demo v0.2")
    print()
    print("Classical view: execute steps in sequence to produce output")
    print("STOCRS-R view: resolve admissible structure to reveal output")
    print()
    print("Principle: output = resolve(structure)")
    print("Law: output_visible iff structure_complete AND structure_consistent")
    print()
    print("Base final total:", result["base_final_total"])
    print("Same structure same output:", "YES" if result["same_structure_same_output"] else "NO")
    print("Same structure same certificate:", "YES" if result["same_structure_same_certificate"] else "NO")
    print()
    print("Reusable template final total:", result["reused_template_final_total"])
    print("Enhanced final total:", result["enhanced_final_total"])
    print("Enhancement improves total:", "YES" if result["enhancement_improves_total"] else "NO")
    print("Enhancement savings:", result["enhancement_savings"])
    print()
    print("Incomplete state:", result["incomplete_run"]["state"])
    print("Conflict state:", result["conflict_run"]["state"])
    print()
    print("Created:", OUT_JSON)
    print("Created:", OUT_VERIFY)
    print("Demo certificate:", result["demo_certificate"])


if __name__ == "__main__":
    main()
