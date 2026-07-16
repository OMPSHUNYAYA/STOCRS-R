# 🧩 STOCRS-R Proof Sketch

## Deterministic Structural Resolution and Versioned Program Evolution

**Reference:** STOCRS-R v1.0  
**Profile:** `STOCRS-R-STRUCTURAL-RESOLUTION-1-D01`  
**Schema:** `1.0.0`  
**Rulebook:** `STOCRS-R-RULEBOOK-1-D01`

---

## Purpose

This document provides a bounded proof sketch for the deterministic properties demonstrated by the STOCRS-R v1.0 reference implementation.

STOCRS-R is a deterministic structural-resolution reference model. It separates:

- the declared program definition
- declared inputs
- evidence
- available nodes
- resolution state
- supported output
- versioned program identity
- deterministic resolution certificates

The current reference model is intentionally narrower than the general statement:

`same structure -> same output`

Its governing relation is:

`same program identity + same declared inputs + same evidence + same available-node set + complete presentation of that set -> same supported values`

For the complete semantic resolution state:

`same semantic resolution inputs -> same state + same certificate`

The current implementation also demonstrates:

`claim multiplicity != structural authority`

and:

`declared rule mutation -> new program identity -> deterministic new supported output`

This document is a proof sketch of those bounded properties. It is not a machine-checked formal proof and does not claim universal sequence independence for arbitrary software.

---

# 1. Model and Definitions

Let a STOCRS-R resolution case be described by:

`X = (P, I, E, A, T, R)`

where:

- `P` = declared program definition
- `I` = declared inputs
- `E` = submitted evidence or claims
- `A` = available-node set
- `T` = target node
- `R` = frozen resolver semantics and rulebook

The reference resolver also receives a presentation order for the nodes in `A`.

For the presentation-order result demonstrated by v1.0, the presentation is required to be complete:

`every node in the tested available-node set is presented to the resolver`

The order may differ, but the tested set does not.

The declared program contains finite nodes of two kinds:

- input nodes
- derived nodes

A derived node contains:

- declared dependencies
- a rule identity
- declared rule parameters

The supported rule set in the reference implementation is finite and explicit.

---

## 1.1 Program Identity

The reference implementation computes:

`program_identity = SHA256(canonical program payload)`

The payload binds:

`profile + schema version + rulebook identity + canonical program definition`

The canonical program definition includes:

- node identity
- node kind
- dependency list
- rule identity
- rule parameters

Program nodes are serialized deterministically by node identity.

Therefore, within the current representation:

`same canonical program definition -> same program identity`

Different frozen program definitions are expected to produce different SHA-256 identities under standard cryptographic hash assumptions.

The mathematical determinism of the resolver rests on equality of the declared semantic inputs.

The SHA-256 value is a compact verification fingerprint of those declared inputs; it is not a proof that cryptographic collisions are impossible.

---

## 1.2 Declared-Input Identity

Declared inputs are identified separately from the program:

`declared_input_identity = SHA256(canonical declared inputs)`

Therefore:

`same program + different declared inputs`

does not imply:

`same supported output`

The reference demonstration explicitly verifies:

`different declared inputs -> different declared-input identity`

while reusing the same program definition.

---

## 1.3 Evidence Identity

Evidence is normalized before it receives an identity.

For each claimed node:

- a scalar claim is treated as a one-element claim list
- duplicate identical claims are collapsed
- distinct claims are serialized deterministically
- claim ordering does not determine authority

The reference implementation computes:

`evidence_identity = SHA256(canonical normalized evidence)`

Therefore repeated identical evidence does not gain additional authority merely through repetition.

---

## 1.4 Resolution Result

For a case `X`, the resolver produces a semantic result containing fields including:

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

The result is then assigned a resolution certificate.

---

# 2. Deterministic Resolution Theorem

## Statement

For the frozen STOCRS-R v1.0 resolver, assume:

1. the same canonical program definition
2. the same declared inputs
3. the same normalized evidence
4. the same available-node set
5. complete presentation of that same available-node set
6. the same target node
7. the same frozen rulebook and resolver semantics

Then the resolver produces the same:

- supported values
- unresolved set
- missing-input set
- conflict set
- blocked set
- resolution frontiers
- resolution state
- output visibility
- supported output
- resolution certificate

within the supported reference environment.

---

## Proof Sketch

### Step 1 — Initial supported inputs are deterministic

For every presented available input node, the resolver performs one of two deterministic actions:

- if a declared input exists, its declared value becomes supported
- otherwise, the node becomes unresolved and is recorded as a missing input

Because the program, declared inputs, available-node set, and complete presented set are fixed, the initial supported-value set, unresolved set, and missing-input set are fixed.

---

### Step 2 — The ready frontier is deterministic

A derived node is ready exactly when all of its declared dependencies already have supported values.

Therefore:

`ready(n) iff every dependency of n is supported`

At any resolution stage, the ready-node set is determined only by:

- the fixed program definition
- the current supported values
- the current unresolved nodes

The ready set is then sorted deterministically.

Therefore the next resolution frontier is deterministic.

---

### Step 3 — Every supported rule application is deterministic

Each reference rule maps fixed dependency values and fixed rule parameters to one result.

For example:

`MULTIPLY`

`ADD`

`THRESHOLD_VALUE`

`SUBTRACT`

`PERCENT_ROUND`

`ZERO_IF_THRESHOLD_ELSE_VALUE`

`SUM_ROUND`

Under the frozen implementation semantics:

`same rule + same dependency values + same parameters -> same result`

Therefore every node resolved in a frontier receives the same value in repeated equivalent cases.

---

### Step 4 — Frontier induction preserves equality

Assume two equivalent resolution cases have identical supported values before frontier `k`.

By Step 2, they compute the same ready frontier.

By Step 3, every node in that frontier receives the same supported value.

Therefore both cases have identical supported values after frontier `k`.

By induction over all resolvable frontiers:

`same semantic resolution inputs -> same supported values`

---

### Step 5 — Resolution terminates deterministically

The declared program is finite.

Whenever a non-empty frontier is resolved, at least one unresolved derived node is removed from the unresolved set.

Therefore the frontier loop cannot continue indefinitely.

It stops when no additional derived node can be supported.

At that point, the final supported-value set and unresolved set are deterministic.

---

### Step 6 — Conflict evaluation is deterministic

Normalized evidence is compared against the deterministically supported values.

Each claim receives one of the current deterministic outcomes, including:

- compatible claim
- `unknown_claim_node`
- `multi_value_conflict`
- `claim_without_supported_value`
- `claim_vs_structure`

Therefore the conflict map is deterministic.

---

### Step 7 — Conflict propagation is deterministic

When conflicts exist, STOCRS-R computes the structural descendants of the conflicting nodes.

The blocked set is the deterministic dependency closure of those conflict roots.

Supported values belonging to blocked nodes are removed from visible supported values.

Therefore the final visible-value map is deterministic.

---

### Step 8 — State and output visibility are deterministic

The current state rule is:

`if conflicts exist -> CONFLICT`

`else if unresolved nodes remain -> INCOMPLETE`

`else -> RESOLVED`

The visibility rule is:

`output_visible iff state = RESOLVED AND target_node is supported`

Therefore the state, output visibility, and supported final output are deterministic.

This establishes the bounded resolution result.

---

# 3. Presentation-Order Independence

## Statement

Within the v1.0 reference model:

`reordering the complete presentation of the same available-node set does not change the tested supported result`

The demonstration verifies:

`same_program_same_inputs_same_output: PASS`

`same_program_same_inputs_same_state: PASS`

`same_program_same_inputs_same_certificate: PASS`

`same_program_identity_under_reordered_presentation: PASS`

---

## Proof Sketch

The initial presentation loop may encounter nodes in different orders, but:

- supported values are stored by node identity
- unresolved nodes are stored as a set
- missing inputs are stored as a set
- every tested available node is presented
- resolution readiness is determined from dependency satisfaction
- each ready frontier is sorted deterministically

Therefore, after complete presentation of the same node set, the initial semantic collections are equivalent regardless of presentation order.

The frontier process then depends on dependency readiness, not the original presentation sequence.

Hence, for the tested model:

`same complete presented node set + same semantic resolution inputs -> same resolution result`

---

## Boundary of This Result

This result concerns:

`presentation ordering of the same declared nodes in the STOCRS-R reference resolver`

It does not establish that all real-world software is independent of:

- execution order
- message order
- concurrency behavior
- side effects
- synchronization
- networking
- persistence
- orchestration
- timing

The current claim is narrower:

`presentation order is not result authority for the demonstrated resolution cases`

Operational execution still exists.

The resolver itself executes deterministic rules.

The demonstrated property is that the tested node-presentation order does not determine the supported result.

---

# 4. Resolution-State Boundary

The reference implementation exposes three top-level states:

## `RESOLVED`

No conflict is present and no unresolved presented available node remains.

A supported final output is visible only when the target node is also supported.

## `INCOMPLETE`

No conflict is present, but one or more presented available nodes remain unresolved.

## `CONFLICT`

One or more evidence conflicts are present.

`CONFLICT` takes precedence over `INCOMPLETE` in the top-level state classification.

---

## Visibility Law

The exact reference visibility rule is:

`output_visible iff state = RESOLVED AND target_node is supported`

Therefore:

`INCOMPLETE -> no supported final output`

`CONFLICT -> no supported final output`

and:

`RESOLVED + unsupported target -> no supported final output`

This is a result-suppression rule within the declared reference model.

It prevents the resolver from presenting an unsupported target value as a resolved final output.

---

# 5. Incomplete-State Safety

## Statement

If a required declared input is absent and the affected dependency structure is presented to the resolver, the unresolved dependency chain remains explicit.

In the reference demonstration:

`ITEM_B_PRICE` is removed from the declared inputs.

The result is:

`state = INCOMPLETE`

`output_visible = false`

`supported_output = null`

---

## Proof Sketch

A missing input node cannot receive a supported value.

Any derived node requiring that value cannot become ready.

Any downstream node that depends on that unresolved chain also remains unresolved.

Therefore the target cannot be supported through that dependency chain.

When no conflict exists and unresolved nodes remain:

`state = INCOMPLETE`

The visibility rule then guarantees:

`output_visible = false`

Thus the reference resolver does not force a final supported output from the demonstrated incomplete case.

---

# 6. Conflict Safety

## Statement

Evidence disagreement does not select a winner by repetition or majority.

The current reference relation is:

`claim multiplicity != structural authority`

---

## 6.1 Compatible Repetition

For:

`ITEM_A_PRICE: [120, 120]`

normalization collapses duplicate identical claims to one unique claim:

`[120, 120] -> [120]`

The claim agrees with the supported value.

Therefore the case remains:

`RESOLVED`

Repeated compatible evidence does not alter the structurally supported value.

---

## 6.2 Multi-Value Conflict

For:

`ITEM_A_PRICE: [120, 999]`

normalization preserves the two distinct values.

Because more than one distinct value remains:

`len(unique claims) > 1`

the result is:

`multi_value_conflict`

and the case becomes:

`CONFLICT`

---

## 6.3 Unanimous Unsupported Claim

For:

`ITEM_A_PRICE: [999, 999]`

duplicate repetition is collapsed:

`[999, 999] -> [999]`

The remaining claim disagrees with the supported declared input value.

Therefore:

`claim_vs_structure`

and:

`state = CONFLICT`

Repetition does not transform an unsupported value into authority.

---

## 6.4 Reverse-Majority Claim

For:

`ITEM_A_PRICE: [999, 999, 120]`

normalization produces the distinct claim set:

`[120, 999]`

The number of times either value appeared before normalization does not select a winner.

Therefore:

`multi_value_conflict`

and:

`state = CONFLICT`

---

## 6.5 Wrong Derived Claim

For:

`FINAL_TOTAL: 999`

the declared program and inputs support:

`FINAL_TOTAL = 330.0`

The conflicting claim therefore produces:

`claim_vs_structure`

The target becomes blocked and the final output is not visible.

---

# 7. Claim-Multiplicity Invariance

## Statement

For repeated copies of one identical claim value `v`:

`normalize([v]) = normalize([v, v]) = normalize([v, v, ..., v])`

Therefore:

`repetition count alone does not change normalized evidence`

and:

`repetition count alone does not increase structural authority`

---

## Proof Sketch

Evidence normalization stores unique values using their deterministic serialized form.

All identical copies of `v` have the same serialized form.

They therefore collapse to one normalized value.

Hence identical repetition does not alter:

- normalized evidence content
- evidence identity
- structural comparison outcome

For competing distinct values, normalization preserves the distinct alternatives and produces a conflict rather than a majority decision.

This directly establishes the demonstrated relation:

`claim multiplicity != structural authority`

---

# 8. Deterministic Certificates

Each resolution case receives a SHA-256 certificate derived from its canonical semantic result payload.

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

`same semantic resolution inputs -> same semantic result payload -> same certificate`

subject to the deterministic canonical serialization and standard SHA-256 assumptions used by the reference implementation.

---

## 8.1 What the Certificate Does Not Mean

A STOCRS-R resolution certificate is not, by itself:

- proof that the declared business rules are correct
- proof that the declared inputs are truthful
- proof of real-world validity
- proof of legal, financial, safety, or domain correctness
- a production certification

It is a reproducible identity for the canonical structural-resolution artifact produced by the declared reference model.

---

## 8.2 Three Distinct Verification Objects

The current repository distinguishes:

`file hash -> frozen script identity`

`resolution certificate -> canonical case identity`

`demo certificate -> aggregate reference-demonstration identity`

These objects serve different purposes and should not be treated as interchangeable.

---

# 9. Program Identity and Versioned Evolution

STOCRS-R v1.0 separates:

`resolver continuity`

from:

`program identity change`

The resolver and rulebook may remain fixed while the declared program definition changes.

Because program identity binds the canonical program definition, a declared change to:

- nodes
- dependencies
- rule identity
- rule parameters

changes the program payload and therefore changes its program fingerprint under the current identity scheme.

---

## Enhancement Relation

The reference demonstration establishes the bounded relation:

`declared rule mutation -> new program identity -> deterministic new supported output`

The demonstration contains:

- base program
- enhanced program v1
- enhanced program v2

The reference results are:

`base program -> 330.0`

`enhanced program v1 -> 313.5`

`enhanced program v2 -> 302.5`

The enhanced v1 to v2 policy change is:

`coupon amount: 15 -> 25`

The resolver and rulebook remain fixed.

The program identity changes from:

`229d4cfe911ce842e71e4bb9aef489f5e75a42245eea12bf1543271b49699247`

to:

`724ee987ad45da92d9c0fa517abb5613c9ea666a36af69b99130f0b09feab4cd`

The supported result changes deterministically from:

`313.5`

to:

`302.5`

This demonstrates versioned program evolution without requiring a different resolver implementation for the demonstrated policy change.

---

# 10. Reuse of One Program with Different Inputs

The same base program is also resolved using a second declared-input set.

The program identity remains:

`5dcf47c311d9633cc97fe92c3aad31d541ef1aa3ecf1eee8efed6e16808502cb`

while the declared-input identity changes.

The supported result changes from:

`330.0`

to:

`374.0`

Therefore:

`same program identity != same output when declared inputs differ`

This is why the current STOCRS-R invariant explicitly includes declared inputs.

The accurate relation is not:

`same program -> same output`

It is:

`same program + same semantic resolution inputs -> same supported result`

within the declared model.

---

# 11. Replay Stability

For an unchanged semantic resolution case, repeated invocation of the frozen resolver produces the same semantic result.

Therefore:

`resolve(X) = resolve(X)`

for the same declared case `X`.

The reference demonstration verifies repeated equivalent cases with reordered node presentation and obtains:

- identical supported output
- identical state
- identical program identity
- identical resolution certificate

This is the current replay-stability result.

It does not imply that arbitrary external systems, side effects, nondeterministic services, or unconstrained environments will automatically reproduce the same behavior.

---

# 12. Canonicalization Boundary

STOCRS-R uses deterministic serialization to create stable identities.

The current canonicalization guarantees are implementation-specific.

In particular, the v1.0 program identity normalizes program-node mapping order, while preserving declared structural content such as dependency lists, rule identities, and rule parameters.

Therefore the current identity should be understood as:

`canonical identity of the declared v1.0 program representation`

It is not a claim that every semantically equivalent program written in a different representation, language, graph encoding, or algebraic form must receive the same identity.

Similarly, the certificate is canonical for the declared v1.0 semantic payload.

It is not a universal representation-independent equivalence proof.

---

# 13. Resolution Authority and Execution

STOCRS-R does not claim that execution disappears.

The reference implementation itself executes:

- input loading
- dependency checks
- rule application
- evidence normalization
- conflict detection
- descendant blocking
- state classification
- hashing

The distinction demonstrated by STOCRS-R is narrower:

`the tested presentation order does not act as the authority that selects the supported result`

Within the frozen model, supported values are determined by:

- the declared program
- declared inputs
- normalized evidence
- available nodes
- frozen rules

Operational systems may still be required for:

- running the resolver
- persistence
- communication
- orchestration
- interfaces
- deployment
- monitoring
- scaling

STOCRS-R separates deterministic structural resolution from those broader operational concerns.

---

# 14. Relationship to Declarative and Constraint Systems

STOCRS-R is not presented as a replacement for:

- declarative programming
- rule engines
- Datalog
- constraint solvers
- workflow systems
- general-purpose programming

Its current reference focus is:

- explicit program identity
- separate declared-input identity
- separate evidence identity
- deterministic dependency resolution
- explicit incompleteness
- conflict-aware output suppression
- non-majoritarian claim handling
- replay-verifiable result certificates
- versioned program evolution through declared rule changes

These properties may coexist with existing programming and execution systems.

---

# 15. What the Proof Sketch Establishes

Within the declared STOCRS-R v1.0 reference model, the proof sketch supports the following bounded statements:

- fixed semantic resolution inputs produce deterministic supported values
- equivalent complete node presentation does not change the tested result
- missing required inputs remain explicitly unresolved
- conflicting evidence prevents supported final-output visibility
- identical repeated claims do not gain authority through multiplicity
- mixed competing claims produce conflict rather than majority selection
- unsupported unanimous claims do not override the structurally supported value
- wrong derived-value claims are rejected
- deterministic program identity is separate from declared-input identity
- declared rule changes produce versioned program identities
- the same resolver can resolve multiple declared program versions
- resolution certificates are reproducible identities of canonical semantic result payloads

---

# 16. What the Proof Sketch Does Not Establish

The current reference model does not establish:

- universal sequence independence for all software
- universal synchronization independence
- elimination of execution environments
- elimination of programming languages
- elimination of orchestration, networking, persistence, or coordination
- distributed consensus
- equivalence of all semantically similar program representations
- collision-free cryptographic identity in the mathematical sense
- universal performance or scalability guarantees
- production safety certification
- correctness of arbitrary domain rules
- truthfulness of externally supplied inputs
- real-world superiority over existing programming paradigms

These boundaries are part of the proof statement, not exceptions to it.

---

# 17. Falsification Targets

The STOCRS-R v1.0 claims are intended to be directly challengeable.

A counterexample within the declared model would be significant if it demonstrated that:

- identical semantic resolution inputs produce different supported values
- identical semantic resolution inputs produce different certificates
- complete reordering of the same tested available-node set changes the supported result
- a missing required input still produces the demonstrated supported final output
- conflicting evidence is silently accepted as supported truth
- repeated unsupported claims override the declared structural result
- a majority of repeated claims selects a winner
- a frozen rule-parameter change leaves the demonstrated canonical program identity unchanged
- repeated equivalent runs under the supported reference environment produce different aggregate results

Such a counterexample would identify a failure in the implementation or in the bounded invariant stated here.

---

# 18. Practical Verification

All current reference properties can be reproduced from the repository root with:

```bash
python demo/stocrs_resolution_demo_v1_0.py
```

Expected final status:

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

# 19. Compact Proof Summary

Let:

`X = same declared semantic resolution inputs`

Then, under the frozen STOCRS-R v1.0 resolver:

`X -> same initial supported inputs`

`-> same deterministic ready frontiers`

`-> same deterministic rule results`

`-> same supported values`

`-> same normalized evidence comparison`

`-> same conflicts and blocked descendants`

`-> same unresolved state`

`-> same resolution state`

`-> same output visibility`

`-> same supported output`

`-> same canonical semantic payload`

`-> same resolution certificate`

Therefore:

`same semantic resolution inputs -> same state + same certificate`

For the tested complete presentation-order permutations:

`same semantic resolution inputs + same complete available-node set -> same supported result`

For program evolution:

`declared rule mutation -> changed program definition -> new program identity -> deterministic new supported output`

For claim authority:

`claim multiplicity != structural authority`

These are the central bounded guarantees demonstrated by STOCRS-R v1.0.

---

# Scope Note

This proof sketch applies exclusively to the declared STOCRS-R v1.0 reference model and its frozen rulebook, program representation, resolution semantics, and verification artifacts.

The current implementation uses:

- Python 3.9+
- the Python standard library
- deterministic JSON serialization
- SHA-256 identities and certificates

The project does not currently include built-in:

- persistence
- distributed resolution
- large-scale orchestration
- formal machine-checked proofs
- production certification

Performance and scalability have not yet been established through formal large-scale benchmarking.

Production use requires independent validation and domain-specific testing.

---

# Final Statement

STOCRS-R v1.0 demonstrates a precise and bounded proposition:

**A declared program can be resolved deterministically from explicit program structure, declared inputs, normalized evidence, available nodes, and frozen rules without allowing the tested node-presentation order or claim repetition to become result authority.**

Its central relations are:

`same program identity + same declared inputs + same evidence + same available-node set + complete presentation of that set -> same supported values`

`same semantic resolution inputs -> same state + same certificate`

`claim multiplicity != structural authority`

`declared rule mutation -> new program identity -> deterministic new supported output`

Execution remains necessary to run the system.

The narrower STOCRS-R contribution is that, within the declared reference model, deterministic structural resolution determines the supported result while the tested presentation order does not.

This is STOCRS-R v1.0.

---

## Cross-Document Consistency

This proof sketch is aligned with the current:

- STOCRS-R README
- Verification Guide
- reference Python implementation
- generated JSON result
- generated verification summary
- frozen demo SHA-256

For practical verification, run:

`python demo/stocrs_resolution_demo_v1_0.py`

and compare the generated artifacts with the committed reference outputs.
