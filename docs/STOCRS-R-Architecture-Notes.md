# ⭐ STOCRS-R — Architecture Notes

## Deterministic Structural Resolution and Versioned Program Evolution

**Reference:** STOCRS-R v1.0  
**Profile:** `STOCRS-R-STRUCTURAL-RESOLUTION-1-D01`  
**Schema:** `1.0.0`  
**Rulebook:** `STOCRS-R-RULEBOOK-1-D01`

**Deterministic • Structure-Driven • Conflict-Aware • Replay-Verifiable**

---

# 1. Architectural Purpose

STOCRS-R defines a bounded structural-resolution architecture in which a declared program is resolved from explicit semantic inputs rather than allowing node-presentation order or claim repetition to become result authority.

The v1.0 reference model separates:

- declared program definition
- declared inputs
- evidence
- available nodes
- target node
- frozen resolver semantics
- resolution state
- supported output
- program identity
- deterministic resolution certificates

Its current governing relation is:

`same program identity + same declared inputs + same evidence + same available-node set + complete presentation of that set -> same supported values`

For the complete semantic resolution state:

`same semantic resolution inputs -> same state + same certificate`

The reference implementation also demonstrates:

`claim multiplicity != structural authority`

and:

`declared rule mutation -> new program identity -> deterministic new supported output`

The architecture is intentionally bounded.

It does not claim that execution disappears or that arbitrary software is universally independent of sequence, synchronization, timing, or orchestration.

---

# 2. Core Architectural Principle

A STOCRS-R resolution case can be described as:

`X = (P, I, E, A, T, R)`

where:

- `P` = declared program definition
- `I` = declared inputs
- `E` = submitted evidence or claims
- `A` = available-node set
- `T` = target node
- `R` = frozen resolver semantics and rulebook

The current reference architecture resolves:

`resolve(P, I, E, A, T, R)`

The architecture therefore does not reduce correctness to a single undifferentiated object called "structure."

It explicitly distinguishes:

`program definition != declared inputs != evidence != node availability != resolution result`

This separation is essential because:

`same program + different inputs -> potentially different output`

and:

`same resolver + changed program definition -> new program identity`

---

## 2.1 Architectural Invariant

Within the frozen STOCRS-R v1.0 model:

`same semantic resolution inputs -> same semantic resolution result`

The current semantic resolution result includes:

- supported values
- unresolved nodes
- missing inputs
- conflicts
- blocked nodes
- resolution frontiers
- resolution state
- output visibility
- supported output

The corresponding certificate relation is:

`same semantic resolution inputs -> same state + same certificate`

subject to the deterministic canonical serialization and SHA-256 identity scheme used by the reference implementation.

---

## 2.2 Presentation-Order Boundary

The v1.0 demonstration verifies that reordering the complete presentation of the same available-node set does not change the tested:

- supported output
- resolution state
- program identity
- resolution certificate

The bounded relation is:

`same semantic resolution inputs + same complete available-node set -> same tested resolution result`

This does not establish universal order independence for arbitrary:

- concurrent systems
- message streams
- side-effecting applications
- distributed workflows
- databases
- networks
- orchestration systems

The architectural claim is narrower:

`node-presentation order is not result authority for the demonstrated reference cases`

---

# 3. High-Level Architecture

STOCRS-R can be understood through five conceptual layers.

---

## 3.1 Program Definition Layer

Responsible for declaring:

- node identities
- node kinds
- dependency relationships
- rule identities
- rule parameters

The program definition is canonicalized and bound to a deterministic program identity.

Program identity includes:

`profile + schema version + rulebook identity + canonical program definition`

This layer determines the frozen program being resolved.

It does not include the current declared input values.

---

## 3.2 Resolution Input Layer

Responsible for supplying:

- declared inputs
- evidence or claims
- available-node set
- target node

Declared inputs receive a separate deterministic identity.

Evidence is normalized and receives a separate deterministic identity.

This separation prevents the architecture from treating:

`same program identity`

as equivalent to:

`same complete resolution case`

---

## 3.3 Structural Resolution Layer

Responsible for:

- loading supported input values
- tracking unresolved nodes
- identifying missing inputs
- resolving deterministic dependency frontiers
- applying frozen rules
- comparing evidence against supported values
- detecting conflicts
- blocking conflict descendants
- classifying the final resolution state
- determining output visibility

This is the core STOCRS-R resolver.

Its output states are:

- `RESOLVED`
- `INCOMPLETE`
- `CONFLICT`

---

## 3.4 Verification Layer

Responsible for producing reproducible identities for:

- program definition
- declared inputs
- normalized evidence
- individual resolution cases
- aggregate demonstration output
- frozen source files

The current repository distinguishes:

`program identity`

`declared-input identity`

`evidence identity`

`resolution certificate`

`demo certificate`

`file SHA-256`

These verification objects serve different purposes.

They should not be treated as interchangeable.

---

## 3.5 Operational and Interface Layer

Responsible for capabilities such as:

- running the resolver
- persistence
- communication
- APIs
- user interfaces
- dashboards
- deployment
- orchestration
- monitoring
- scaling

This layer remains operationally necessary where an application requires those capabilities.

STOCRS-R does not claim to eliminate execution infrastructure.

The architectural distinction is that, within the reference model, those operational mechanisms do not determine the supported result by altering node-presentation order or claim multiplicity.

---

# 4. Program Data Model

---

## 4.1 Input Nodes

An input node declares:

- `kind = input`
- no dependencies
- rule identity `DECLARED_INPUT`

Its value is supplied through the declared-input map.

If an available input node has no corresponding declared input, that node becomes:

- unresolved
- recorded as missing

---

## 4.2 Derived Nodes

A derived node declares:

- `kind = derived`
- dependency list
- rule identity
- rule parameters

A derived node becomes ready only when all of its declared dependencies have supported values.

The readiness condition is:

`ready(node) iff every declared dependency has a supported value`

---

## 4.3 Supported Reference Rules

The current v1.0 reference implementation includes a finite explicit rule set:

- `MULTIPLY`
- `ADD`
- `THRESHOLD_VALUE`
- `SUBTRACT`
- `PERCENT_ROUND`
- `ZERO_IF_THRESHOLD_ELSE_VALUE`
- `SUM_ROUND`

For each frozen rule:

`same rule + same dependency values + same parameters -> same result`

within the supported Python reference environment.

---

# 5. Program Identity Model

The current program identity is computed from a canonical payload containing:

- profile
- schema version
- rulebook identity
- canonical program definition

The canonical program definition contains:

- node identity
- node kind
- dependency list
- rule identity
- rule parameters

Program nodes are serialized deterministically by node identity.

Therefore:

`same canonical program definition -> same program identity`

Different program payloads are expected to produce different SHA-256 fingerprints under the current identity scheme.

The hash serves as a compact verification fingerprint.

It is not a mathematical proof that cryptographic collisions are impossible.

---

## 5.1 Program Identity Is Not Input Identity

Declared input values are deliberately excluded from program identity.

Therefore:

`same program identity + different declared inputs -> potentially different supported output`

The reference demonstration verifies this directly.

The same base program produces:

`330.0`

for one declared-input set and:

`374.0`

for another.

The program identity remains unchanged while the declared-input identity changes.

---

# 6. Declared-Input Identity

Declared inputs receive a separate canonical identity:

`declared_input_identity = SHA256(canonical declared inputs)`

This allows STOCRS-R to distinguish:

`program reuse`

from:

`program mutation`

Program reuse:

`same program identity + different declared-input identity`

Program mutation:

`different canonical program definition -> different program identity`

This distinction is central to versioned structural resolution.

---

# 7. Evidence and Claim Model

Evidence is treated as a separate semantic input.

For each claimed node:

- a scalar claim becomes a one-element list
- identical duplicates are collapsed
- distinct values are preserved
- claim order does not select authority
- repetition count does not select authority

The governing relation is:

`claim multiplicity != structural authority`

---

## 7.1 Compatible Repetition

Example:

`ITEM_A_PRICE: [120, 120]`

normalizes to:

`[120]`

If `120` is the structurally supported value, the claim is compatible.

Repeated compatible evidence does not alter the supported value.

---

## 7.2 Conflicting Distinct Claims

Example:

`ITEM_A_PRICE: [120, 999]`

produces:

`multi_value_conflict`

The resolver does not select a majority or preferred value.

---

## 7.3 Repeated Unsupported Claim

Example:

`ITEM_A_PRICE: [999, 999]`

normalizes to:

`[999]`

If the supported declared input is `120`, the result is:

`claim_vs_structure`

Repetition does not create authority.

---

## 7.4 Reverse-Majority Claim

Example:

`ITEM_A_PRICE: [999, 999, 120]`

normalizes to the distinct values:

`[120, 999]`

The result is:

`multi_value_conflict`

The number of repetitions does not select a winner.

---

# 8. Resolution Algorithm

The core resolver proceeds through deterministic stages.

---

## 8.1 Stage 1 — Load Presented Available Nodes

The resolver considers nodes that are:

- present in the available-node set
- present in the declared program
- included in the supplied presentation

For the current presentation-order guarantee, the tested presentation is complete with respect to the available-node set.

---

## 8.2 Stage 2 — Resolve Declared Inputs

For each presented input node:

`declared value exists -> supported value`

`declared value missing -> unresolved + missing input`

---

## 8.3 Stage 3 — Build Ready Frontiers

Among unresolved derived nodes, a node becomes ready when:

`all declared dependencies are supported`

The ready set is sorted deterministically.

That sorted set becomes the next resolution frontier.

---

## 8.4 Stage 4 — Apply Frozen Rules

Every ready node is evaluated using:

- its declared rule identity
- its declared dependencies
- its declared parameters
- already supported dependency values

Resolved nodes are removed from the unresolved set.

The process repeats until no additional node is ready.

Because the declared program is finite and each non-empty frontier removes at least one unresolved derived node, the frontier process terminates.

---

## 8.5 Stage 5 — Evaluate Evidence

Normalized evidence is compared against supported values.

The current conflict types include:

- `unknown_claim_node`
- `multi_value_conflict`
- `claim_without_supported_value`
- `claim_vs_structure`

Compatible evidence does not create a conflict.

---

## 8.6 Stage 6 — Propagate Conflict Blocking

If a node conflicts, the resolver computes its dependency descendants.

Conflicting nodes and their descendants form the blocked set.

Blocked values are removed from the visible supported-value map.

This prevents a value downstream of conflicting evidence from remaining visible as an unaffected supported value.

---

## 8.7 Stage 7 — Classify Resolution State

The current precedence rule is:

`if conflicts exist -> CONFLICT`

`else if unresolved nodes remain -> INCOMPLETE`

`else -> RESOLVED`

Therefore:

`CONFLICT` takes precedence over `INCOMPLETE`

at the top-level state.

---

## 8.8 Stage 8 — Determine Output Visibility

The exact reference rule is:

`output_visible iff state = RESOLVED AND target_node is supported`

Therefore:

`INCOMPLETE -> no supported final output`

`CONFLICT -> no supported final output`

`RESOLVED + unsupported target -> no supported final output`

The architecture does not infer a target result merely because some other nodes are supported.

---

# 9. Resolution States

---

## 9.1 `RESOLVED`

A case is `RESOLVED` when:

- no evidence conflict exists
- no presented available node remains unresolved

A final supported output is visible only if the target node is also supported.

---

## 9.2 `INCOMPLETE`

A case is `INCOMPLETE` when:

- no evidence conflict exists
- one or more presented available nodes remain unresolved

The reference demonstration includes a missing-input case in which:

`ITEM_B_PRICE`

is absent.

The resulting state is:

`INCOMPLETE`

with:

`output_visible = false`

`supported_output = null`

---

## 9.3 `CONFLICT`

A case is `CONFLICT` when evidence:

- contains multiple distinct values for one claimed node
- disagrees with a structurally supported value
- claims an unsupported value
- refers to an unknown node

A `CONFLICT` case does not expose a supported final output.

---

# 10. Deterministic Presentation-Order Property

The base reference program is evaluated using different seeded node-presentation orders.

The v1.0 demonstration verifies:

`same_program_same_inputs_same_output: PASS`

`same_program_same_inputs_same_state: PASS`

`same_program_same_inputs_same_certificate: PASS`

`same_program_identity_under_reordered_presentation: PASS`

The architectural explanation is:

- initial values are stored by node identity
- unresolved nodes are stored as a set
- missing inputs are stored as a set
- complete presentation contains the same tested node set
- readiness depends on dependency satisfaction
- every ready frontier is sorted deterministically

Therefore the tested presentation order does not act as result authority.

---

## 10.1 Boundary of the Property

This property does not imply that STOCRS-R has eliminated:

- execution order from all software
- synchronization from distributed systems
- concurrency hazards
- side effects
- message ordering
- orchestration
- persistence ordering
- networking requirements

It demonstrates a narrower property of the reference resolver:

`reordering the complete presentation of the same available nodes does not change the tested semantic result`

---

# 11. Certificate Architecture

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
- target node
- supported output
- supported values
- unresolved nodes
- missing inputs
- conflicts
- blocked nodes
- deterministic resolution frontiers

The current relation is:

`same semantic resolution inputs -> same semantic payload -> same certificate`

within the frozen reference model.

---

## 11.1 What the Certificate Represents

The resolution certificate is a reproducible fingerprint of the canonical semantic result payload.

It supports:

- replay comparison
- reference verification
- change detection
- case identity comparison

---

## 11.2 What the Certificate Does Not Prove

The certificate does not independently prove:

- truthfulness of declared inputs
- correctness of business policy
- legal correctness
- financial correctness
- safety certification
- real-world validity
- universal semantic equivalence

It identifies the result produced by the declared frozen model.

---

# 12. Verification Object Separation

STOCRS-R v1.0 separates several verification identities.

---

## 12.1 Program Identity

Identifies:

`the canonical declared program definition`

---

## 12.2 Declared-Input Identity

Identifies:

`the canonical declared input set`

---

## 12.3 Evidence Identity

Identifies:

`the canonical normalized evidence set`

---

## 12.4 Resolution Certificate

Identifies:

`the canonical semantic result of one resolution case`

---

## 12.5 Demo Certificate

Identifies:

`the aggregate committed reference-demonstration result`

Current expected demo certificate:

`b9933beee7810d44be54face75313aa69204fe963536e6ca67d31844cb2c4530`

---

## 12.6 Frozen File SHA-256

Identifies:

`the exact committed source file bytes`

Current frozen reference script SHA-256:

`5f9f248546674fbf9e67be3956c7db2e0029a7c9c5965b055665a291a799fa95`

These identities serve different verification roles.

---

# 13. Versioned Program Evolution

STOCRS-R separates:

`resolver continuity`

from:

`program identity change`

A declared program may evolve while the resolver and rulebook remain unchanged.

The current bounded enhancement relation is:

`declared rule mutation -> new program identity -> deterministic new supported output`

---

## 13.1 Base Program

Current base result:

`330.0`

Current base program identity:

`5dcf47c311d9633cc97fe92c3aad31d541ef1aa3ecf1eee8efed6e16808502cb`

---

## 13.2 Enhanced Program v1

Adds a loyalty-coupon branch and resolves to:

`313.5`

Program identity:

`229d4cfe911ce842e71e4bb9aef489f5e75a42245eea12bf1543271b49699247`

---

## 13.3 Enhanced Program v2

Changes the declared coupon amount:

`15 -> 25`

and resolves to:

`302.5`

Program identity:

`724ee987ad45da92d9c0fa517abb5613c9ea666a36af69b99130f0b09feab4cd`

---

## 13.4 Architectural Interpretation

The resolver does not need to be rewritten for the demonstrated policy change.

Instead:

`same resolver + same rulebook + changed declared program -> new versioned program identity`

This enables explicit comparison between:

- resolver change
- program change
- input change
- evidence change

Those are architecturally different events.

---

# 14. Replay Stability

For the same semantic resolution case:

`resolve(X) = resolve(X)`

Repeated equivalent runs produce the same:

- supported values
- state
- supported output
- resolution certificate

The current reference demonstration also verifies this property under reordered complete node presentation.

This is a replay-stability property of the frozen reference model.

It is not a claim that arbitrary external dependencies or nondeterministic services are automatically reproducible.

---

# 15. Safety Model

---

## 15.1 Missing Information

Missing required input produces explicit unresolved structure.

The resolver does not invent a replacement value.

---

## 15.2 Conflicting Evidence

Conflicting evidence produces:

`CONFLICT`

The resolver does not force a majority winner.

---

## 15.3 Unsupported Claims

An unsupported claim does not override the value supported by the declared program and inputs.

---

## 15.4 Downstream Conflict Containment

Structural descendants of conflicting nodes are blocked from remaining visible as unaffected supported values.

---

## 15.5 Final-Output Suppression

The target output is visible only when:

`state = RESOLVED`

and:

`target node is supported`

This is the reference model's primary output-safety boundary.

---

# 16. Relationship to Execution Systems

STOCRS-R does not define an execution-free architecture.

The reference implementation itself performs deterministic execution.

Operational systems may still be needed for:

- computation
- persistence
- communication
- scheduling
- deployment
- monitoring
- user interaction
- distributed coordination

The STOCRS-R distinction is:

`operational execution exists`

while:

`the tested node-presentation order and claim multiplicity do not select the supported result`

Within the reference model, the supported result is determined by:

- declared program definition
- declared inputs
- normalized evidence
- available nodes
- frozen resolver semantics

---

# 17. Relationship to Declarative and Constraint-Based Systems

STOCRS-R shares characteristics with existing declarative, rule-based, dependency-driven, and constraint-oriented systems.

It is not positioned as a replacement for:

- declarative programming
- Datalog
- rule engines
- constraint solvers
- workflow systems
- general-purpose programming

Its current architectural focus is the combination of:

- explicit program identity
- separate input identity
- separate evidence identity
- deterministic dependency resolution
- explicit incompleteness
- conflict-aware output suppression
- non-majoritarian claim handling
- deterministic case certificates
- versioned program evolution

These properties can coexist with conventional execution and orchestration systems.

---

# 18. Architectural Comparison

| Concern | Conventional Operational Approach | STOCRS-R v1.0 Reference Approach |
|---|---|---|
| Program definition | Often embedded in executable code or configuration | Explicit canonical program definition |
| Inputs | Runtime data | Separately identified declared inputs |
| Evidence | Application-specific | Separately normalized and identified claims |
| Missing information | Often error, default, retry, or exception | Explicit unresolved state |
| Conflicting claims | Application-specific reconciliation | Explicit conflict; no majority selection |
| Node presentation | May affect procedural execution | Tested complete presentation order does not select result |
| Program evolution | Code/configuration change | Explicit program-identity change |
| Replay comparison | Logs, outputs, traces | Canonical semantic certificate |
| Source integrity | File checksums | Separate frozen SHA-256 |

This table describes the STOCRS-R reference architecture.

It does not imply that conventional systems cannot implement similar properties.

---

# 19. Architecture Boundaries

The current v1.0 architecture does not establish:

- universal sequence independence
- universal synchronization independence
- distributed consensus
- transactional durability
- production-grade persistence
- large-scale orchestration
- cross-language semantic equivalence
- automatic equivalence of differently encoded programs
- cryptographic collision impossibility
- universal performance guarantees
- domain correctness of supplied rules
- truthfulness of supplied data
- safety-critical certification

The reference architecture is deliberately bounded and falsifiable.

---

# 20. Falsification Targets

A significant counterexample within the declared model would include:

- identical semantic resolution inputs producing different supported values
- identical semantic resolution inputs producing different certificates
- complete reordering of the same tested available-node set changing the supported result
- repeated unsupported claims overriding the declared structural result
- majority repetition selecting a winner
- missing required input still producing the demonstrated supported final output
- conflicting evidence remaining silently accepted
- a declared rule-parameter change failing to change the canonical program payload
- repeated equivalent runs producing different aggregate reference results

These are direct architectural challenge points.

---

# 21. Practical Verification

Run from the repository root:

```bash
python demo/stocrs_resolution_demo_v1_0.py
```

Expected:

`ALL CHECKS: PASS`

The current demonstration performs 15 checks:

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

Expected demo certificate:

`b9933beee7810d44be54face75313aa69204fe963536e6ca67d31844cb2c4530`

Expected frozen script SHA-256:

`5f9f248546674fbf9e67be3956c7db2e0029a7c9c5965b055665a291a799fa95`

---

# 22. Current Architectural Guarantees

Within the declared STOCRS-R v1.0 reference model:

- fixed semantic resolution inputs produce deterministic supported values
- equivalent complete node presentation does not change the tested result
- missing required inputs remain explicitly unresolved
- conflicting evidence suppresses final supported-output visibility
- repeated identical claims do not gain authority through multiplicity
- competing distinct claims produce conflict rather than majority selection
- wrong derived-value claims are rejected
- program identity is separate from input identity
- evidence identity is separate from program identity
- one frozen resolver can resolve multiple declared program versions
- the demonstrated declared rule mutations produce explicit versioned program-identity changes
- canonical semantic result payloads receive reproducible resolution certificates

---

# 23. Relationship to the Shunyaya Framework

STOCRS-R belongs to the broader Shunyaya structural-resolution direction.

Its specific architectural contribution is bounded to:

`deterministic structural application resolution + explicit versioned program evolution`

Within that scope, STOCRS-R demonstrates that operational ordering need not be the sole authority over a supported result when the reference resolver is given the same complete semantic resolution inputs.

This is consistent with the broader Shunyaya dependency-elimination principle:

`operational dependency may remain while no longer serving as the sole resolution authority`

For STOCRS-R v1.0, the demonstrated dependency boundary is:

`node-presentation order is not the sole authority over the tested supported result`

The implementation does not claim elimination of execution itself.

---

# 24. Unified Architectural Principle

The STOCRS-R v1.0 architecture can be summarized as:

`declare the program`

`identify the inputs`

`normalize the evidence`

`resolve supported dependency frontiers`

`preserve incompleteness`

`reject conflict`

`expose the target only when resolved`

`bind the semantic result to a reproducible certificate`

For program evolution:

`change the declared program -> change the program identity -> resolve the new version deterministically`

---

# 25. Final Architectural Statement

STOCRS-R v1.0 defines a bounded deterministic structural-resolution architecture in which:

**A declared program is resolved from explicit program structure, declared inputs, normalized evidence, available nodes, and frozen rules without allowing the tested node-presentation order or claim repetition to become result authority.**

Its central relations are:

`same program identity + same declared inputs + same evidence + same available-node set + complete presentation of that set -> same supported values`

`same semantic resolution inputs -> same state + same certificate`

`claim multiplicity != structural authority`

`declared rule mutation -> new program identity -> deterministic new supported output`

Execution remains necessary to run the resolver and any surrounding system.

The architectural contribution is narrower and more precise:

**within the declared STOCRS-R v1.0 reference model, deterministic structural resolution determines the supported result while the tested presentation order and claim repetition do not.**

---

## Cross-Document Consistency

These architecture notes are aligned with the current:

- STOCRS-R README
- Proof Sketch
- Verification Guide
- reference Python implementation
- generated JSON result
- generated verification summary
- frozen demo SHA-256

For reproducible verification, run:

`python demo/stocrs_resolution_demo_v1_0.py`

and compare the generated outputs with the committed reference artifacts.
