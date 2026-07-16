# STOCRS-R Verification Guide

## Structural Resolution Reference Demonstration v1.0

**Profile:** `STOCRS-R-STRUCTURAL-RESOLUTION-1-D01`  
**Schema:** `1.0.0`  
**Rulebook:** `STOCRS-R-RULEBOOK-1-D01`

---

## 1. Purpose

This guide defines the recommended verification procedure for the STOCRS-R v1.0 reference demonstration.

The current implementation demonstrates a bounded deterministic structural-resolution model in which:

`same program identity + same declared inputs + same evidence + same available-node set -> same supported values`

`same semantic resolution inputs -> same state + same certificate`

`claim multiplicity != structural authority`

`declared rule mutation -> new program identity -> deterministic new supported output`

The reference implementation uses Python 3.9+ and the standard library only.

---

## 2. Reference Files

Current authoritative demonstration:

`demo/stocrs_resolution_demo_v1_0.py`

Generated reference outputs:

`outputs/STOCRS_R_Demo_v1_0.json`

`outputs/STOCRS_R_Demo_v1_0_VERIFY.txt`

Frozen script hash:

`VERIFY/FREEZE_DEMO_SHA256.txt`

---

## 3. Run the Reference Demonstration

From the repository root:

`python demo/stocrs_resolution_demo_v1_0.py`

From inside the `demo` folder:

`python stocrs_resolution_demo_v1_0.py`

The demonstration regenerates the current JSON and verification output files in the repository `outputs/` folder.

---

## 4. Expected Summary

Expected values:

`Base final total: 330.0`

`Reused template final total: 374.0`

`Enhanced final total v1: 313.5`

`Enhanced final total v2: 302.5`

Expected final status:

`ALL CHECKS: PASS`

Expected demo certificate:

`b9933beee7810d44be54face75313aa69204fe963536e6ca67d31844cb2c4530`

---

## 5. Expected Program Identities

Base program identity:

`5dcf47c311d9633cc97fe92c3aad31d541ef1aa3ecf1eee8efed6e16808502cb`

Enhanced program v1 identity:

`229d4cfe911ce842e71e4bb9aef489f5e75a42245eea12bf1543271b49699247`

Enhanced program v2 identity:

`724ee987ad45da92d9c0fa517abb5613c9ea666a36af69b99130f0b09feab4cd`

The enhanced program identities differ because the declared program definition changes.

The v1 to v2 enhancement changes the coupon policy parameter from `15` to `25`.

The rulebook and resolver remain fixed while the program identity changes.

---

## 6. Required Verification Checks

The reference demonstration performs 15 checks.

Expected:

`same_program_same_inputs_same_output: PASS`

`same_program_same_inputs_same_state: PASS`

`same_program_same_inputs_same_certificate: PASS`

`same_program_identity_under_reordered_presentation: PASS`

`different_inputs_change_input_identity: PASS`

`incomplete_input_stays_incomplete: PASS`

`compatible_repeated_claim_resolves: PASS`

`multi_value_claim_conflicts: PASS`

`unanimous_wrong_claim_rejected: PASS`

`reverse_majority_cannot_override: PASS`

`wrong_derived_claim_rejected: PASS`

`enhancement_v1_program_identity_differs_from_base: PASS`

`policy_update_changes_program_identity: PASS`

`enhancement_v1_resolves: PASS`

`enhancement_v2_resolves: PASS`

Final expected result:

`ALL CHECKS: PASS`

---

## 7. Deterministic Presentation-Order Check

The base program is resolved twice using different seeded presentation orders.

Expected:

`same_program_same_inputs_same_output: PASS`

`same_program_same_inputs_same_state: PASS`

`same_program_same_inputs_same_certificate: PASS`

`same_program_identity_under_reordered_presentation: PASS`

This demonstrates that, within the reference model, reordering the presentation of the same declared program nodes does not change the tested supported result, state, certificate, or program identity.

This is a bounded reference result.

It does not claim that all real-world software execution is independent of sequence or synchronization.

---

## 8. Declared Inputs and Program Identity

STOCRS-R v1.0 separates declared inputs from the program definition.

Program identity binds:

`profile + schema + rulebook + canonical program definition`

The canonical program definition includes:

- node identity
- node kind
- dependencies
- rule identity
- rule parameters

Declared inputs receive a separate deterministic identity.

Therefore:

`same program identity + different declared inputs -> potentially different supported output`

while:

`same program identity + same declared inputs + same evidence + same available-node set -> same supported values`

within the current deterministic reference model.

---

## 9. Incomplete-State Verification

The incomplete case removes one required declared input:

`ITEM_B_PRICE`

Expected:

`state: INCOMPLETE`

`output_visible: false`

`supported_output: null`

The unresolved set records the nodes that cannot complete because the required input is missing.

No supported final output is exposed.

---

## 10. Conflict Verification

STOCRS-R v1.0 treats claim multiplicity as evidence, not authority.

Core relation:

`claim multiplicity != structural authority`

### Compatible repeated claim

Example:

`ITEM_A_PRICE: [120, 120]`

Expected:

`RESOLVED`

Repeated compatible evidence does not change the structurally supported value.

### Multi-value conflict

Example:

`ITEM_A_PRICE: [120, 999]`

Expected:

`CONFLICT`

Conflict type:

`multi_value_conflict`

The affected node and its structural descendants do not remain visible as supported values.

### Unanimous wrong claim

Example:

`ITEM_A_PRICE: [999, 999]`

Expected:

`CONFLICT`

Conflict type:

`claim_vs_structure`

Repeated agreement on an unsupported value does not override the declared input.

### Reverse-majority claim

Example:

`ITEM_A_PRICE: [999, 999, 120]`

Expected:

`CONFLICT`

Conflict type:

`multi_value_conflict`

The number of repetitions does not select a winner.

### Wrong derived-value claim

Example:

`FINAL_TOTAL: 999`

Expected:

`CONFLICT`

Conflict type:

`claim_vs_structure`

A claim cannot override the value supported by the declared program and inputs.

---

## 11. Structural Enhancement Verification

The demonstration includes:

- base program
- enhanced program v1
- enhanced program v2

The base program resolves to:

`330.0`

Enhanced program v1 resolves to:

`313.5`

Enhanced program v2 resolves to:

`302.5`

The enhancement model demonstrates:

`declared rule mutation -> new program identity -> deterministic new supported output`

The coupon policy parameter changes from `15` to `25`.

Because the policy parameter is part of the canonical program definition:

`enhanced_program_v1_identity != enhanced_program_v2_identity`

This prevents different frozen program definitions from being represented by the same program identity.

---

## 12. Certificate Verification

Each resolution result receives a SHA-256 certificate derived from its canonical semantic payload.

The payload includes:

- profile
- schema version
- rulebook identity
- program identity
- declared input identity
- evidence identity
- available nodes
- resolution state
- output visibility
- target node
- supported output
- supported values
- unresolved nodes
- missing inputs
- conflicts
- blocked nodes
- deterministic resolution frontiers

For identical semantic resolution inputs under the current reference model:

`same semantic resolution inputs -> same state + same certificate`

The demo certificate is a separate aggregate artifact derived from the identities, check results, and individual case certificates.

---

## 13. Verify Script File Identity

From the repository root on Windows:

`certutil -hashfile demo\stocrs_resolution_demo_v1_0.py SHA256`

Expected SHA-256:

`5f9f248546674fbf9e67be3956c7db2e0029a7c9c5965b055665a291a799fa95`

The result must exactly match:

`VERIFY/FREEZE_DEMO_SHA256.txt`

Important distinction:

`file hash -> identity of the frozen script file`

`resolution certificate -> identity of a canonical structural-resolution artifact`

`demo certificate -> aggregate identity of the reference demonstration result`

These are separate verification objects.

---

## 14. Re-run Verification

Run the demonstration twice without changing the script:

`python demo/stocrs_resolution_demo_v1_0.py`

`python demo/stocrs_resolution_demo_v1_0.py`

Expected:

- identical summary values
- identical program identities
- identical individual case certificates
- identical demo certificate
- `ALL CHECKS: PASS`

The generated output files should reproduce deterministically in the same supported Python environment.

---

## 15. Scope Boundary

The current STOCRS-R release is a bounded reference implementation.

It demonstrates:

- deterministic structural resolution within the declared rulebook
- explicit `RESOLVED`, `INCOMPLETE`, and `CONFLICT` states
- deterministic program identity
- separate declared-input identity
- claim conflict handling
- rejection of unsupported unanimous claims
- rejection of majority-style claim authority
- validation of claims against supported derived values
- tested presentation-order independence
- deterministic structural enhancement through versioned program identity
- reproducible SHA-256 certificates

It does not establish:

- universal sequence independence for all software
- universal synchronization independence
- elimination of execution environments
- elimination of orchestration or networking
- production safety or correctness certification
- distributed consensus
- universal scalability or performance guarantees

Production use requires independent validation and domain-specific testing.

---

## 16. Final Verification Result

A successful reference run must end with:

`ALL CHECKS: PASS`

and:

`Demo certificate: b9933beee7810d44be54face75313aa69204fe963536e6ca67d31844cb2c4530`

The current bounded reference relation is:

`same program identity + same declared inputs + same evidence + same available-node set -> same supported values`

with deterministic certificates for the declared semantic resolution state.

STOCRS-R v1.0 therefore demonstrates a structure-governed reference model in which program identity, declared inputs, frozen rules, explicit incompleteness, and conflict handling determine the supported result within the modeled boundary.
