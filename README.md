# ⭐ STOCRS-R

## STOCRS-Resolution — Deterministic Structural Resolution and Versioned Program Evolution

![STOCRS-R](https://img.shields.io/badge/STOCRS--R-Structural%20Resolution-black)
![Version](https://img.shields.io/badge/Reference-v1.0-blue)
![Deterministic](https://img.shields.io/badge/Resolution-Deterministic-green)
![Checks](https://img.shields.io/badge/Checks-15%2F15%20PASS-brightgreen)
![Conflict-Aware](https://img.shields.io/badge/Conflict-Aware-orange)
![Replay-Verified](https://img.shields.io/badge/Replay-Verifiable-blue)
![Python](https://img.shields.io/badge/Python-3.9%2B-blue)

[![STOCRS-R Verify](https://github.com/OMPSHUNYAYA/STOCRS-R/actions/workflows/stocrs-r-verify.yml/badge.svg)](https://github.com/OMPSHUNYAYA/STOCRS-R/actions/workflows/stocrs-r-verify.yml)

---

**Where declared program structure, inputs, evidence, and available nodes determine a supported result within a frozen reference model.**

STOCRS-R is a bounded deterministic reference implementation for structural resolution and versioned program evolution.

Its current core relation is:

`same program identity + same declared inputs + same evidence + same available-node set + complete presentation of that set -> same supported values`

For the full semantic resolution state:

`same semantic resolution inputs + complete presentation of the same available-node set -> same state + same certificate`

The current reference model also enforces:

`claim multiplicity != structural authority`

and:

`declared rule mutation -> new program identity -> deterministic new supported output`

---

![STOCRS-R Structural Resolution and Versioned Program Evolution](docs/STOCRS-R-Diagram.png)

---

## 🌐 STOCRS-R — Structural Resolution Layer

STOCRS-R continues the structural direction explored by [STOCRS](https://github.com/OMPSHUNYAYA/STOCRS), while focusing on a narrower application-level question:

**Can a deterministic resolver preserve explicit program identity, incomplete states, conflict handling, replay-verifiable results, and controlled program evolution without allowing presentation order or claim repetition to become result authority?**

The v1.0 reference implementation answers that question within its declared model.

It separates:

- program identity
- declared-input identity
- evidence identity
- available-node state
- resolution state
- result certificates
- aggregate demonstration identity

This separation allows the resolver to distinguish between:

`same program + different inputs`

`same topology + different rule parameters`

`compatible evidence`

`conflicting evidence`

`missing required inputs`

and:

`unsupported claims`

---

## 🧱 Core Model

STOCRS-R v1.0 uses an explicit deterministic program definition.

Program identity binds:

`profile + schema + rulebook + canonical program definition`

The canonical program definition includes:

- node identity
- node kind
- dependencies
- rule identity
- rule parameters

Declared inputs are identified separately.

Evidence is normalized and identified separately.

The available-node set is also part of the semantic resolution state.

The current bounded relation is therefore:

`same program identity + same declared inputs + same evidence + same available-node set + complete presentation of that set -> same supported values`

The available-node set and its complete presentation are also part of the bounded resolution conditions tested by the reference demonstration.

This relation is intentionally narrower than:

`same structure -> same output`

because STOCRS-R v1.0 explicitly distinguishes the program definition from inputs, evidence, and node availability.

---

## ⚙️ Resolution States

The reference implementation returns one of three top-level states:

### `RESOLVED`

The declared inputs and available nodes support completion, and no conflicting evidence prevents the result from remaining visible.

### `INCOMPLETE`

Required information is missing, so a supported final result is not exposed.

### `CONFLICT`

Evidence conflicts internally or disagrees with the value supported by the declared program and inputs.

The reference visibility rule is:

`output_visible iff state = RESOLVED AND target_node is supported`

---

## 🛡 Claim Authority

STOCRS-R v1.0 does not treat repetition as authority.

Core relation:

`claim multiplicity != structural authority`

Examples from the reference demonstration:

`[120, 120] -> compatible repeated evidence`

`[120, 999] -> multi_value_conflict`

`[999, 999] -> claim_vs_structure`

`[999, 999, 120] -> multi_value_conflict`

A repeated unsupported value does not override the declared structural result.

A numerical majority does not select a winner.

A wrong claim against a derived value is also rejected.

For example:

`FINAL_TOTAL: 999 -> claim_vs_structure`

The declared program, frozen rulebook, declared inputs, and current semantic resolution state remain authoritative within the model.

---

## 🚀 30-Second Demonstration

Run from the repository root:

```bash
python demo/stocrs_resolution_demo_v1_0.py
```

Expected final status:

`ALL CHECKS: PASS`

Expected demo certificate:

`b9933beee7810d44be54face75313aa69204fe963536e6ca67d31844cb2c4530`

The current demonstration performs 15 checks covering:

- deterministic supported output
- deterministic resolution state
- deterministic certificates
- reordered node presentation
- separate input identity
- explicit incompleteness
- compatible repeated evidence
- multi-value conflict
- rejection of unanimous wrong claims
- rejection of majority-style override
- validation of derived-value claims
- base-to-enhanced program identity changes
- rule-parameter identity changes
- deterministic enhanced-program resolution

---

## 🧪 Reference Results

The current reference run produces:

| Case | Supported Final Result |
|---|---:|
| Base program | `330.0` |
| Reused program with different declared inputs | `374.0` |
| Enhanced program v1 | `313.5` |
| Enhanced program v2 | `302.5` |

Current program identities:

**Base program**

`5dcf47c311d9633cc97fe92c3aad31d541ef1aa3ecf1eee8efed6e16808502cb`

**Enhanced program v1**

`229d4cfe911ce842e71e4bb9aef489f5e75a42245eea12bf1543271b49699247`

**Enhanced program v2**

`724ee987ad45da92d9c0fa517abb5613c9ea666a36af69b99130f0b09feab4cd`

The enhanced v1 and v2 programs use the same resolver and rulebook but different declared coupon policy parameters.

The parameter change:

`15 -> 25`

produces a new program identity and a deterministic new supported result.

This demonstrates the bounded enhancement relation:

`declared rule mutation -> new program identity -> deterministic new supported output`

---

## 🔁 Presentation-Order Independence

The base program is evaluated using different seeded node-presentation orders.

Within the current reference case, the runs preserve:

- the same supported output
- the same resolution state
- the same certificate
- the same program identity

The demonstrated relation is limited to presentation ordering of the same declared program nodes under the same semantic resolution inputs.

It does not claim that arbitrary real-world execution order, orchestration, communication, or synchronization is universally irrelevant.

---

## 🧩 Structural Enhancement

STOCRS-R v1.0 treats program evolution as an explicit identity change.

Program identity is recomputed from the canonical program definition, and the demonstrated program changes produce distinct program identities.

That definition includes both structural relationships and frozen rule parameters.

Therefore:

`the demonstrated changed frozen program definitions -> distinct program identities`

The resolver itself can remain unchanged while a declared policy mutation produces a new versioned program identity and a new deterministic supported result.

This creates a clear distinction between:

`resolver continuity`

and:

`program identity change`

The current demonstration uses this distinction to compare:

- a base program
- an enhanced coupon program using `15`
- an enhanced coupon program using `25`

---

## 🔐 Deterministic Certificates

Each resolution case receives a SHA-256 certificate derived from a canonical semantic payload.

The certificate binds fields including:

- profile
- schema version
- rulebook identity
- program identity
- declared-input identity
- evidence identity
- available nodes
- resolution state
- output visibility
- supported output
- supported values
- unresolved nodes
- missing inputs
- conflicts
- blocked nodes
- deterministic resolution frontiers

The current certificate relation is:

`same semantic resolution inputs + complete presentation of the same available-node set -> same state + same certificate`

The demonstration also produces a separate aggregate demo certificate.

---

## 🧪 Current Reference Demonstration

[Run `stocrs_resolution_demo_v1_0.py`](demo/stocrs_resolution_demo_v1_0.py)

Generated reference artifacts:

- [STOCRS_R_Demo_v1_0.json](outputs/STOCRS_R_Demo_v1_0.json)
- [STOCRS_R_Demo_v1_0_VERIFY.txt](outputs/STOCRS_R_Demo_v1_0_VERIFY.txt)

Verification:

- [Verification Guide](VERIFY/VERIFY.md)
- [Frozen Demo SHA-256](VERIFY/FREEZE_DEMO_SHA256.txt)

---

## 🔐 File Integrity Check

### Windows

```powershell
certutil -hashfile demo\stocrs_resolution_demo_v1_0.py SHA256
```

### Linux / macOS

```bash
sha256sum demo/stocrs_resolution_demo_v1_0.py
```

Expected SHA-256:

`5f9f248546674fbf9e67be3956c7db2e0029a7c9c5965b055665a291a799fa95`

This must match:

[VERIFY/FREEZE_DEMO_SHA256.txt](VERIFY/FREEZE_DEMO_SHA256.txt)

Important distinction:

`file hash -> frozen script identity`

`resolution certificate -> canonical case identity`

`demo certificate -> aggregate reference-demonstration identity`

---

## 🔬 What the Current Verification Establishes

Within the declared v1.0 reference model, the demonstration verifies:

- deterministic resolution for the tested cases
- explicit `RESOLVED`, `INCOMPLETE`, and `CONFLICT` states
- stable program identity under reordered presentation
- separate program and declared-input identities
- evidence normalization
- conflict propagation to structural descendants
- rejection of unsupported unanimous claims
- rejection of majority-style claim authority
- validation of claims against supported derived values
- distinct program identities for the demonstrated frozen rule-parameter changes
- reproducible SHA-256 resolution certificates

The reference implementation uses Python 3.9+ and the standard library only.

---

## ⚠️ Scope and Boundaries

STOCRS-R v1.0 is a bounded reference implementation.

It does not establish:

- universal sequence independence for all software
- universal synchronization independence
- elimination of programming languages
- elimination of execution environments
- elimination of orchestration, networking, persistence, or coordination
- replacement of general-purpose software systems
- distributed consensus
- universal performance or scalability guarantees
- production safety or correctness certification

The current implementation does not include built-in persistence, distributed resolution, or large-scale orchestration.

Performance and scalability have not yet been established through formal large-scale benchmarking.

Production use requires independent validation and domain-specific testing.

---

## ❓ Relationship to Declarative Systems

STOCRS-R is not presented as a replacement for declarative programming, rule engines, Datalog, constraint solvers, workflow systems, or general-purpose programming.

Its current reference focus is narrower:

- deterministic structural resolution
- explicit program identity
- explicit input identity
- explicit evidence identity
- safe incompleteness
- conflict-aware result suppression
- replay-verifiable certificates
- versioned program evolution through declared rule changes

These ideas may coexist with existing execution and declarative systems.

---

## 🔥 Falsification Targets

The current reference model is intended to be inspectable and challengeable.

Useful falsification targets include demonstrating, within the declared v1.0 model, that:

- identical semantic resolution inputs with complete presentation of the same available-node set produce different certificates
- reordered presentation of the same tested program changes the supported result
- an incomplete required input still produces a supported final output
- conflicting evidence is silently treated as supported truth
- repeated unsupported claims override the declared structural result
- the demonstrated frozen coupon rule-parameter change leaves program identity unchanged

A demonstrated counterexample within the declared model would identify a failure in the current implementation or its stated invariant.

---

## 🧭 Relationship to STOCRS

[STOCRS](https://github.com/OMPSHUNYAYA/STOCRS) explores deterministic structural computation under explicit incompleteness and conflict-aware resolution.

STOCRS-R continues that direction at the program-resolution layer.

Its current focus is:

`program identity + declared inputs + evidence + available nodes -> supported structural resolution`

and:

`declared rule mutation -> new program identity -> deterministic new supported output`

The two projects therefore address related but distinct questions.

---

## 📚 Documentation

- [Quickstart](docs/Quickstart.md)
- [FAQ](docs/FAQ.md)
- [Proof Sketch](docs/Proof-Sketch.md)
- [STOCRS-R Architecture Notes](docs/STOCRS-R-Architecture-Notes.md)
- [STOCRS-R Enhancement Model](docs/STOCRS-R-Enhancement-Model.md)
- [STOCRS-R Challenge](docs/STOCRS-R-Challenge.md)

Additional visual references:

- [STOCRS-R Concept Diagram](docs/STOCRS-R-Diagram.png)
- [Dependency Elimination Framework](docs/Dependency-Elimination-Framework.png)
- [Shunyaya Structural Stack](docs/Shunyaya-Structural-Stack.png)

---

## 🛡 What STOCRS-R Is / Is Not

### STOCRS-R IS

- a bounded deterministic structural-resolution reference model
- a conflict-aware resolver
- a program-identity demonstration
- a versioned structural-enhancement demonstration
- a replay-verifiable reference implementation

### STOCRS-R IS NOT

- a proof that all software can ignore sequence
- a proof that synchronization is universally unnecessary
- a replacement for execution environments
- a distributed consensus protocol
- a production-certified runtime

---

## 🔭 Research Direction

Future exploration may include:

- reusable structural modules
- declarative structural definitions
- incremental or differential structural resolution
- larger multi-module examples
- property-based testing
- independent verification implementations
- structural replay stress testing
- program-identity visualization
- additional language implementations
- formalized semantics
- machine-checked proofs of precisely stated invariants

Future work should preserve explicit identity boundaries between:

`program`

`declared inputs`

`evidence`

`available nodes`

and:

`resolution state`

---

## 📜 **License**

See: [LICENSE](LICENSE)

The repository is a publicly available reference implementation under its stated license terms.

Use of the software, documentation, architecture, and related materials is governed by the licensing terms declared in the repository.

The repository does not claim recognition as a formal technical standard.

---

## 🧭 Final Statement

STOCRS-R v1.0 does not ask whether execution disappears.

It asks a narrower question:

**Can a declared program be resolved deterministically from explicit structural inputs while preserving incompleteness, rejecting conflicting authority, and assigning a new identity when its frozen rules change?**

The current bounded reference implementation demonstrates that behavior across its declared test cases.

Its central relation is:

`same program identity + same declared inputs + same evidence + same available-node set + complete presentation of that set -> same supported values`

with:

`same semantic resolution inputs + complete presentation of the same available-node set -> same state + same certificate`

and:

`claim multiplicity != structural authority`

For structural evolution:

`declared rule mutation -> new program identity -> deterministic new supported output`

**This is STOCRS-R v1.0.**
