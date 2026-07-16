# ⭐ STOCRS-R — Quickstart

## Deterministic Structural Resolution and Versioned Program Evolution

**Reference:** STOCRS-R v1.0  
**Profile:** `STOCRS-R-STRUCTURAL-RESOLUTION-1-D01`  
**Schema:** `1.0.0`  
**Rulebook:** `STOCRS-R-RULEBOOK-1-D01`

**Deterministic • Structure-Driven • Conflict-Aware • Replay-Verifiable**

---

# What STOCRS-R Demonstrates

STOCRS-R v1.0 is a bounded deterministic reference model for structural resolution and versioned program evolution.

Its current governing relation is:

`same program identity + same declared inputs + same evidence + same available-node set + complete presentation of that set -> same supported values`

For the complete semantic result:

`same semantic resolution inputs + complete presentation of the same available-node set -> same state + same certificate`

The current implementation also demonstrates:

`claim multiplicity != structural authority`

and:

`declared program mutation -> changed canonical program payload -> new program identity -> deterministic new supported output`

STOCRS-R does not claim that execution disappears or that arbitrary software is universally independent of sequence, synchronization, timing, or orchestration.

Its narrower result is that, within the declared v1.0 reference model, the tested node-presentation order and claim repetition do not become result authority.

---

# 30-Second Start

From the repository root, run:

```bash
python demo/stocrs_resolution_demo_v1_0.py
```

Expected final status:

`ALL CHECKS: PASS`

Expected demo certificate:

`b9933beee7810d44be54face75313aa69204fe963536e6ca67d31844cb2c4530`

The demo regenerates the current reference artifacts in:

`outputs/`

---

# Current Reference Results

| Case | Supported Final Result |
|---|---:|
| Base program | `330.0` |
| Reused base program with different declared inputs | `374.0` |
| Enhanced program v1 | `313.5` |
| Enhanced program v2 | `302.5` |

Current program identities:

**Base program**

`5dcf47c311d9633cc97fe92c3aad31d541ef1aa3ecf1eee8efed6e16808502cb`

**Enhanced program v1**

`229d4cfe911ce842e71e4bb9aef489f5e75a42245eea12bf1543271b49699247`

**Enhanced program v2**

`724ee987ad45da92d9c0fa517abb5613c9ea666a36af69b99130f0b09feab4cd`

---

# Minimum Requirements

- Python 3.9+
- Python standard library only
- no external Python packages
- no network connection required for the reference demonstration

---

# Current Repository Layout

The current public release uses one reference demo and two generated output artifacts.

```text
STOCRS-R/

├── README.md
├── LICENSE
│
├── demo/
│   └── stocrs_resolution_demo_v1_0.py
│
├── outputs/
│   ├── STOCRS_R_Demo_v1_0.json
│   └── STOCRS_R_Demo_v1_0_VERIFY.txt
│
├── docs/
│   ├── FAQ.md
│   ├── Proof-Sketch.md
│   ├── Quickstart.md
│   ├── STOCRS-R-Architecture-Notes.md
│   ├── STOCRS-R-Challenge.md
│   ├── STOCRS-R-Enhancement-Model.md
│   ├── STOCRS-R-Diagram.png
│   ├── Dependency-Elimination-Framework.png
│   └── Shunyaya-Structural-Stack.png
│
└── VERIFY/
    ├── VERIFY.md
    └── FREEZE_DEMO_SHA256.txt
```

The earlier demo versions and earlier generated-output sets are not part of the current reference path.

The earlier PDF artifact has also been removed from the current public release.

---

# What the Resolver Receives

A resolution case can be described as:

`X = (P, I, E, A, T, R)`

where:

- `P` = declared program definition
- `I` = declared inputs
- `E` = submitted evidence or claims
- `A` = available-node set
- `T` = target node
- `R` = frozen resolver semantics and rulebook

The reference resolver also receives a node-presentation order.

For the current presentation-order guarantee, the presentation must be complete with respect to the tested available-node set.

---

# Resolution States

The reference implementation returns one of three top-level states.

## `RESOLVED`

No evidence conflict exists and no presented available node remains unresolved.

A final supported output is visible only if the target node is also supported.

## `INCOMPLETE`

No conflict exists, but one or more presented available nodes remain unresolved.

## `CONFLICT`

One or more evidence conflicts exist.

The exact visibility rule is:

`output_visible iff state = RESOLVED AND target_node is supported`

Therefore:

`INCOMPLETE -> no supported final output`

`CONFLICT -> no supported final output`

---

# The 15 Reference Checks

The current v1.0 demonstration performs 15 checks.

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

Expected final line:

`ALL CHECKS: PASS`

---

# Quick Verification Guide

## 1. Run the Reference Demo

From the repository root:

```bash
python demo/stocrs_resolution_demo_v1_0.py
```

Or from inside the `demo` directory:

```bash
python stocrs_resolution_demo_v1_0.py
```

The script writes the current generated artifacts to the repository `outputs/` directory.

---

## 2. Check the Generated Summary

Open:

`outputs/STOCRS_R_Demo_v1_0_VERIFY.txt`

Confirm:

`ALL CHECKS: PASS`

and:

`Demo certificate: b9933beee7810d44be54face75313aa69204fe963536e6ca67d31844cb2c4530`

---

## 3. Inspect the Full Generated Result

Open:

`outputs/STOCRS_R_Demo_v1_0.json`

This artifact contains the detailed reference cases, including:

- program identities
- declared-input identities
- evidence identities
- supported values
- unresolved nodes
- missing inputs
- conflicts
- blocked nodes
- deterministic frontiers
- resolution states
- supported outputs
- resolution certificates
- aggregate demo certificate

---

# Presentation-Order Check

The base program is resolved using different seeded node-presentation orders.

The current reference demonstration verifies that, for the same complete available-node set and equivalent semantic resolution inputs, the tested runs preserve:

- the same supported output
- the same resolution state
- the same program identity
- the same resolution certificate

This is the demonstrated relation:

`same semantic resolution inputs + complete presentation of the same available-node set -> same tested resolution result`

This does not mean that arbitrary execution order is irrelevant in all software.

It means that the tested complete node-presentation order does not select the result in this reference resolver.

---

# Incomplete-State Check

The reference demo removes:

`ITEM_B_PRICE`

from the declared inputs.

Expected:

`state = INCOMPLETE`

`output_visible = false`

`supported_output = null`

The resolver leaves the affected dependency chain unresolved rather than inventing a replacement value.

---

# Conflict Checks

STOCRS-R treats claim multiplicity as evidence, not authority.

Core relation:

`claim multiplicity != structural authority`

## Compatible repeated claim

```text
ITEM_A_PRICE: [120, 120]
```

Expected:

`RESOLVED`

Identical repetition collapses to one unique normalized value.

---

## Distinct competing claims

```text
ITEM_A_PRICE: [120, 999]
```

Expected:

`CONFLICT`

Conflict type:

`multi_value_conflict`

---

## Repeated unsupported claim

```text
ITEM_A_PRICE: [999, 999]
```

Expected:

`CONFLICT`

Conflict type:

`claim_vs_structure`

Repeated agreement does not override the declared supported value.

---

## Reverse-majority attempt

```text
ITEM_A_PRICE: [999, 999, 120]
```

Expected:

`CONFLICT`

Conflict type:

`multi_value_conflict`

The number of repetitions does not select a winner.

---

## Wrong derived claim

```text
FINAL_TOTAL: 999
```

Expected:

`CONFLICT`

Conflict type:

`claim_vs_structure`

The unsupported claim does not replace the structurally supported result.

---

# Versioned Program Evolution

STOCRS-R separates:

`resolver continuity`

from:

`program identity change`

The current demonstration includes:

- base program
- enhanced program v1
- enhanced program v2

The same resolver and rulebook evaluate all three demonstrated program versions.

The central bounded enhancement relation is:

`declared program mutation -> changed canonical program payload -> new program identity -> deterministic new supported output`

---

## Base to Enhanced v1

Enhanced v1 adds:

- `LOYALTY_COUPON`
- `AFTER_COUPON`

and changes selected dependencies.

Result:

`330.0 -> 313.5`

Program identity:

`5dcf47c311d9633cc97fe92c3aad31d541ef1aa3ecf1eee8efed6e16808502cb`

becomes:

`229d4cfe911ce842e71e4bb9aef489f5e75a42245eea12bf1543271b49699247`

---

## Enhanced v1 to Enhanced v2

The coupon parameter changes:

`15 -> 25`

Result:

`313.5 -> 302.5`

Program identity:

`229d4cfe911ce842e71e4bb9aef489f5e75a42245eea12bf1543271b49699247`

becomes:

`724ee987ad45da92d9c0fa517abb5613c9ea666a36af69b99130f0b09feab4cd`

The demonstrated program changes receive different program identities.

---

# Program Identity vs Input Identity

The same base program is also resolved with different declared inputs.

The program identity remains unchanged.

The supported result changes:

`330.0 -> 374.0`

The declared-input identity changes separately.

Therefore:

`same program identity != same output when declared inputs differ`

This is why the STOCRS-R invariant explicitly includes declared inputs.

---

# Resolution Certificates

Each resolution case receives a SHA-256 certificate derived from a canonical semantic result payload.

The certificate binds fields including:

- profile
- schema version
- rulebook identity
- program identity
- declared-input identity
- evidence identity
- available nodes
- state
- output visibility
- target node
- supported output
- supported values
- unresolved nodes
- missing inputs
- conflicts
- blocked nodes
- deterministic resolution frontiers

The accurate relation is:

`same semantic resolution inputs + complete presentation of the same available-node set -> same state + same certificate`

within the frozen reference model.

---

# Verification Objects

The current repository distinguishes:

`program identity -> canonical declared program`

`declared-input identity -> canonical declared inputs`

`evidence identity -> canonical normalized evidence`

`resolution certificate -> canonical semantic result for one case`

`demo certificate -> aggregate reference-demonstration identity`

`file SHA-256 -> exact reference script bytes`

These are different verification objects.

They should not be treated as interchangeable.

---

# File Integrity Check

Current frozen reference script:

`demo/stocrs_resolution_demo_v1_0.py`

Expected SHA-256:

`5f9f248546674fbf9e67be3956c7db2e0029a7c9c5965b055665a291a799fa95`

## Windows

From the repository root:

```text
certutil -hashfile demo\stocrs_resolution_demo_v1_0.py SHA256
```

## Linux / macOS

```bash
sha256sum demo/stocrs_resolution_demo_v1_0.py
```

Compare the result with:

`VERIFY/FREEZE_DEMO_SHA256.txt`

---

# Determinism Check

Run the demo twice:

```bash
python demo/stocrs_resolution_demo_v1_0.py
```

```bash
python demo/stocrs_resolution_demo_v1_0.py
```

Under the same supported environment and unchanged reference files, expected:

- `ALL CHECKS: PASS`
- same generated reference results
- same demo certificate

For individual equivalent resolution cases with complete presentation of the same available-node set, expected:

- same supported values
- same state
- same supported output
- same resolution certificate

---

# What STOCRS-R Demonstrates

Within the declared v1.0 reference model:

- fixed semantic resolution inputs with complete presentation of the same available-node set produce deterministic supported values
- complete reordering of the tested available-node set does not change the tested result
- missing required inputs remain explicitly unresolved
- conflicting evidence prevents final supported-output visibility
- repeated identical claims do not gain authority through multiplicity
- competing distinct claims produce conflict rather than majority selection
- unsupported unanimous claims do not override the supported structural value
- wrong derived-value claims are rejected
- program identity is separate from declared-input identity
- evidence identity is separate from program identity
- the same resolver can evaluate multiple declared program versions
- the demonstrated program mutations produce explicit versioned program-identity changes
- canonical semantic result payloads receive reproducible resolution certificates

---

# What STOCRS-R Does Not Claim

The current reference model does not establish:

- universal sequence independence for all software
- universal synchronization independence
- elimination of execution environments
- elimination of programming languages
- elimination of networking, persistence, orchestration, or coordination
- distributed consensus
- automatic equivalence of differently encoded programs
- cryptographic collision impossibility
- universal performance or scalability guarantees
- correctness of arbitrary domain rules
- truthfulness of externally supplied inputs
- production safety certification
- automatic migration of arbitrary software systems

The project is a bounded deterministic reference implementation.

---

# Relationship to Execution

Execution remains necessary to run the resolver.

Operational systems may also remain necessary for:

- persistence
- communication
- APIs
- user interfaces
- deployment
- orchestration
- monitoring
- scaling

The STOCRS-R distinction is narrower:

`the tested node-presentation order and claim multiplicity do not select the supported result`

within the declared reference model.

---

# Recommended Reading Order

For a complete review of STOCRS-R:

1. `README.md`
2. `docs/Quickstart.md`
3. `VERIFY/VERIFY.md`
4. `docs/Proof-Sketch.md`
5. `docs/STOCRS-R-Architecture-Notes.md`
6. `docs/STOCRS-R-Enhancement-Model.md`
7. `docs/STOCRS-R-Challenge.md`

The implementation and generated evidence remain the primary executable reference:

`demo/stocrs_resolution_demo_v1_0.py`

`outputs/STOCRS_R_Demo_v1_0.json`

`outputs/STOCRS_R_Demo_v1_0_VERIFY.txt`

---

# Final Summary

STOCRS-R v1.0 demonstrates a bounded deterministic structural-resolution model in which:

`same program identity + same declared inputs + same evidence + same available-node set + complete presentation of that set -> same supported values`

and:

`same semantic resolution inputs + complete presentation of the same available-node set -> same state + same certificate`

It also demonstrates:

`claim multiplicity != structural authority`

and:

`declared program mutation -> changed canonical program payload -> new program identity -> deterministic new supported output`

Execution remains part of the system.

The narrower result is that, within the declared reference model, the tested node-presentation order and claim repetition do not become result authority.

Run:

```bash
python demo/stocrs_resolution_demo_v1_0.py
```

Confirm:

`ALL CHECKS: PASS`

Then inspect the generated artifacts in:

`outputs/`

This is the STOCRS-R v1.0 Quickstart.
