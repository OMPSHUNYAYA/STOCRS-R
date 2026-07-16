# ⭐ STOCRS-R — Enhancement Model

## Deterministic Versioned Program Evolution

**Reference:** STOCRS-R v1.0  
**Profile:** `STOCRS-R-STRUCTURAL-RESOLUTION-1-D01`  
**Schema:** `1.0.0`  
**Rulebook:** `STOCRS-R-RULEBOOK-1-D01`

**Deterministic • Versioned • Structure-Driven • Replay-Verifiable**

---

# Purpose

This document defines the versioned program-evolution model demonstrated by STOCRS-R v1.0.

The enhancement model is useful because STOCRS-R does more than resolve one frozen program.

The reference implementation also demonstrates that:

- one resolver can evaluate multiple declared program versions
- the demonstrated declared program changes receive distinct program identities
- input changes remain separate from program changes
- rule-parameter changes are included in program identity
- upgraded program versions remain independently replayable
- the resulting supported output is determined by the declared version and its semantic resolution inputs

The central bounded relation is:

`declared program mutation -> changed canonical program payload -> new program identity -> deterministic new supported output`

For the exact demonstrated v1.0 cases:

`base program -> 330.0`

`enhanced program v1 -> 313.5`

`enhanced program v2 -> 302.5`

The resolver and rulebook remain unchanged across those demonstrated program versions.

---

# 1. Why a Separate Enhancement Model Exists

STOCRS-R distinguishes several kinds of change that are often combined in application evolution.

These include:

- program change
- rule-parameter change
- declared-input change
- evidence change
- available-node change
- resolver change
- rulebook change

The enhancement model makes those differences explicit.

A change in declared inputs is not automatically a new program.

A change in evidence is not automatically a new program.

A change in the canonical declared program definition is a program-version change.

This distinction allows STOCRS-R to compare application evolution without conflating:

`new data`

with:

`new program`

or:

`new evidence`

with:

`new resolver semantics`

---

# 2. Core Enhancement Principle

Let:

`P_A = base declared program`

`P_B = changed declared program`

and:

`A_A = complete available-node set for P_A`

`A_B = complete available-node set for P_B`

Using the same frozen resolver semantics and rulebook, and the same declared inputs, evidence, and target where applicable:

`resolve(P_A, I, E, A_A, T, R) -> Result_A`

`resolve(P_B, I, E, A_B, T, R) -> Result_B`

When the canonical program definitions differ, their program payloads differ.

Under the current SHA-256 identity scheme, the demonstrated changed program payloads produce different program identities.

Therefore the v1.0 enhancement pattern is:

`same resolver + same rulebook + changed declared program -> versioned program identity + deterministic resolution`

The architecture does not require a different resolver implementation for the demonstrated program changes.

---

# 3. Program Identity Is the Version Boundary

The current program identity binds:

`profile + schema version + rulebook identity + canonical program definition`

The canonical program definition includes:

- node identity
- node kind
- dependency list
- rule identity
- rule parameters

Therefore a declared change to any of these can change the canonical program payload.

Examples include:

- adding a node
- removing a node
- changing a dependency
- changing a rule identity
- changing a rule parameter

For the demonstrated v1.0 program changes, the resulting program identities are different.

The SHA-256 value is a compact fingerprint of the canonical program payload.

It is not a mathematical proof that cryptographic collisions are impossible.

---

# 4. Base Program and Enhanced Programs

The current reference demonstration includes three declared program versions.

---

## 4.1 Base Program

The base program contains:

- two item prices
- two item quantities
- item totals
- subtotal
- threshold discount
- after-discount amount
- tax
- shipping
- final total

Current supported result:

`330.0`

Current program identity:

`5dcf47c311d9633cc97fe92c3aad31d541ef1aa3ecf1eee8efed6e16808502cb`

---

## 4.2 Enhanced Program v1

Enhanced program v1 extends the base program with:

- `LOYALTY_COUPON`
- `AFTER_COUPON`

It also changes the dependency used by:

- `TAX`
- `FINAL_TOTAL`

The declared coupon amount is:

`15`

Current supported result:

`313.5`

Current program identity:

`229d4cfe911ce842e71e4bb9aef489f5e75a42245eea12bf1543271b49699247`

---

## 4.3 Enhanced Program v2

Enhanced program v2 retains the enhanced structure but changes the declared coupon amount:

`15 -> 25`

Current supported result:

`302.5`

Current program identity:

`724ee987ad45da92d9c0fa517abb5613c9ea666a36af69b99130f0b09feab4cd`

---

# 5. The Demonstrated Enhancement Relation

The v1.0 reference demonstration establishes two distinct forms of program evolution.

---

## 5.1 Structural Extension

The transition:

`base program -> enhanced program v1`

changes the declared program structure by introducing new nodes and dependency relationships.

The resolver remains the same.

The rulebook remains the same.

The program identity changes.

The supported output changes deterministically.

This demonstrates:

`declared structural extension -> new canonical program payload -> new program identity -> deterministic new supported output`

---

## 5.2 Policy-Parameter Mutation

The transition:

`enhanced program v1 -> enhanced program v2`

changes one declared rule parameter:

`coupon amount: 15 -> 25`

The resolver remains the same.

The rulebook remains the same.

The broader enhanced topology remains the same.

Because rule parameters are part of the canonical program definition, the demonstrated parameter change produces:

- a different canonical program payload
- a different program identity
- a different deterministic supported output

This demonstrates:

`declared policy-parameter mutation -> versioned program identity change -> deterministic new supported output`

---

# 6. Resolver Continuity

The current enhancement demonstration does not rebuild or replace the resolver.

The same resolution machinery continues to perform:

- input loading
- dependency readiness checks
- deterministic frontier formation
- rule application
- evidence normalization
- conflict detection
- descendant blocking
- state classification
- certificate generation

The changing element is the declared program definition.

Therefore the demonstrated relation is:

`resolver continuity + declared program evolution`

This is one of the main reasons the enhancement model is useful as a separate STOCRS-R document.

It makes clear that:

`program evolution != resolver evolution`

Those events may occur independently.

---

# 7. Enhancement Does Not Mean Same Output

A changed program is allowed to produce a changed supported output.

Therefore STOCRS-R does not claim:

`program mutation -> output preservation`

The actual relation is:

`changed declared program -> potentially changed supported output`

The requirement is deterministic resolution of each declared program version under equivalent semantic resolution conditions.

For one frozen program version:

`same semantic resolution inputs + complete presentation of the same available-node set -> same supported result`

Across different program versions:

`different canonical program definitions -> outputs may differ`

This is expected behavior.

---

# 8. Input Change Is Not Program Enhancement

The reference demonstration also reuses the base program with a second declared-input set.

The base program identity remains:

`5dcf47c311d9633cc97fe92c3aad31d541ef1aa3ecf1eee8efed6e16808502cb`

The supported result changes:

`330.0 -> 374.0`

This is not a program-version change.

It is:

`same program + different declared inputs`

The declared-input identity changes separately.

This distinction prevents STOCRS-R from falsely treating every output change as a program enhancement.

---

# 9. Evidence Change Is Not Program Enhancement

Evidence is also identified separately from the program.

Therefore:

`same program + different evidence`

does not automatically imply:

`different program version`

Evidence may change:

- compatibility state
- conflict state
- certificate
- output visibility

without changing the canonical program definition.

Program identity therefore remains a version boundary for the declared program itself.

---

# 10. Available-Node Change Is Not Program Enhancement

The available-node set is part of the semantic resolution case.

It is not part of the program identity.

Therefore:

`same program + different available-node set`

is not automatically a program mutation.

It is a different resolution condition for the same declared program.

This distinction matters because node availability can affect:

- supported values
- unresolved state
- final resolution state
- certificate

without changing the program definition.

---

# 11. Enhancement Resolution Flow

The current STOCRS-R enhancement flow can be represented as:

`declare base program`

`-> canonicalize program`

`-> compute program identity`

`-> resolve with declared semantic inputs`

`-> record supported result and certificate`

Then:

`change declared program`

`-> canonicalize changed program`

`-> compute new program identity`

`-> resolve with declared semantic inputs`

`-> record new supported result and certificate`

The resolver does not infer that a changed program is equivalent to the earlier version.

The identity change remains explicit.

---

# 12. Enhancement Safety

Program evolution does not bypass the normal STOCRS-R state model.

Every declared program version is still subject to:

- missing-input handling
- unresolved dependency handling
- evidence normalization
- conflict detection
- descendant blocking
- output-visibility rules

Therefore an enhanced program may still resolve to:

- `RESOLVED`
- `INCOMPLETE`
- `CONFLICT`

The current visibility rule remains:

`output_visible iff state = RESOLVED AND target_node is supported`

Enhancement does not grant automatic output visibility.

---

# 13. Replay of Versioned Programs

Each frozen program version can be replayed independently.

For a fixed version:

`same semantic resolution inputs + complete presentation of the same available-node set -> same state + same certificate`

Therefore the reference model supports comparison of:

- base-program replay
- enhanced-program v1 replay
- enhanced-program v2 replay

Each version has its own program identity.

Each resolution case has its own semantic result certificate.

This creates explicit version-scoped replay rather than relying on an unlabelled notion of "the current program."

---

# 14. Certificate Behavior Across Enhancement

A resolution certificate identifies the canonical semantic result payload of one resolution case.

When the program changes, the program identity inside the semantic payload can change.

The supported values, state, output, or frontiers may also change.

Therefore a new program version will generally produce a different resolution certificate for an otherwise comparable case.

The certificate should not be interpreted as:

`the identity of the program alone`

Program identity and resolution certificate are separate verification objects.

---

# 15. Verification Object Separation During Evolution

The enhancement model preserves the distinction between:

`program identity -> canonical declared program`

`declared-input identity -> canonical declared inputs`

`evidence identity -> canonical normalized evidence`

`resolution certificate -> one canonical semantic result`

`demo certificate -> aggregate demonstration identity`

`file SHA-256 -> exact source-file bytes`

This separation makes it possible to determine whether a changed result came from:

- a program change
- an input change
- an evidence change
- an availability change
- a resolver or rulebook change

rather than treating all change as one undifferentiated event.

---

# 16. What "Minimal Mutation" Means Here

STOCRS-R may use a small declared change to produce a new program version.

However, "minimal" is descriptive, not a formal optimization guarantee.

The current demonstration includes:

- one structural extension from the base program to enhanced v1
- one rule-parameter change from enhanced v1 to enhanced v2

The project does not currently prove that these are globally minimal program changes.

The accurate claim is:

`a bounded declared program mutation can be resolved by the same frozen resolver`

and, in the demonstrated cases:

`the mutation produces a new program identity and deterministic new supported output`

---

# 17. What "Reusable Structural Continuity" Means

Within the current reference model, reusable continuity means that unchanged parts of the declared program can remain unchanged while another declared part evolves.

For example:

- the same base input model can be retained
- existing subtotal and discount logic can be retained
- new nodes can be added
- selected dependencies can be redirected
- rule parameters can be changed
- the same resolver can evaluate the resulting version

This is structural reuse within the declared program representation.

It does not mean that arbitrary software systems can always be upgraded without integration work.

---

# 18. Relationship to Declarative and Configuration-Driven Systems

STOCRS-R shares ideas with:

- declarative programming
- rule engines
- configuration-driven systems
- dependency graphs
- dataflow models

Its enhancement model should not be presented as having no precedent in those areas.

The current STOCRS-R contribution is the specific combination of:

- explicit canonical program identity
- separate input identity
- separate evidence identity
- deterministic dependency-frontier resolution
- explicit `INCOMPLETE` and `CONFLICT` states
- non-majoritarian claim handling
- version-scoped semantic certificates
- demonstrated program evolution under one frozen resolver

This combination is the appropriate basis for comparing STOCRS-R with related approaches.

---

# 19. Traditional Evolution vs STOCRS-R Reference Model

| Concern | Common Software Evolution Pattern | STOCRS-R v1.0 Reference Model |
|---|---|---|
| Program change | Code/configuration modification | Explicit canonical program mutation |
| Version identity | Release tag, commit, build, or schema version | Deterministic program identity |
| Input change | Runtime data change | Separate declared-input identity |
| Evidence change | Application-specific | Separate normalized evidence identity |
| Rule-parameter change | Configuration or code change | Included in canonical program identity |
| Resolver reuse | Architecture-dependent | Demonstrated across current program versions |
| Replay comparison | Logs, tests, builds, traces | Version-scoped semantic certificates |
| Incomplete upgraded state | Application-specific | Explicit `INCOMPLETE` |
| Conflicting upgraded evidence | Application-specific | Explicit `CONFLICT` |

This comparison describes the reference model.

It does not imply that conventional systems cannot implement equivalent or stronger versioning mechanisms.

---

# 20. Enhancement Invariants

The current bounded enhancement invariants are:

`same canonical program definition -> same program identity`

`same program identity does not imply same output when declared inputs differ`

`different demonstrated program definitions -> different demonstrated program identities`

`same semantic resolution inputs + complete presentation of the same available-node set -> same state + same certificate`

`declared rule mutation -> new program identity -> deterministic new supported output`

The final relation above describes the demonstrated v1.0 mutations.

It is not a universal cryptographic uniqueness theorem for every possible mutation.

---

# 21. Falsification Targets

A meaningful counterexample within the declared enhancement model would include:

- the same canonical program definition producing inconsistent program identities
- the same frozen program and complete semantic resolution case producing different supported results
- the demonstrated enhanced program resolving nondeterministically
- a declared program mutation being omitted from the canonical program payload
- a declared rule parameter failing to participate in program identity
- the demonstrated policy mutation producing a different result across equivalent complete replays
- input changes being incorrectly encoded as program-identity changes
- evidence changes being incorrectly encoded as program-identity changes

A report should preserve the exact:

- program definition
- program identity
- declared inputs
- evidence
- available-node set
- presentation order
- target node
- resolver version
- rulebook identity
- resulting certificate

---

# 22. Practical Verification

Run from the repository root:

```bash
python demo/stocrs_resolution_demo_v1_0.py
```

Expected final status:

`ALL CHECKS: PASS`

The enhancement-specific checks are:

`enhancement_v1_program_identity_differs_from_base: PASS`

`policy_update_changes_program_identity: PASS`

`enhancement_v1_resolves: PASS`

`enhancement_v2_resolves: PASS`

The broader identity-separation check is:

`different_inputs_change_input_identity: PASS`

Current reference results:

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

Expected demo certificate:

`b9933beee7810d44be54face75313aa69204fe963536e6ca67d31844cb2c4530`

Expected frozen reference script SHA-256:

`5f9f248546674fbf9e67be3956c7db2e0029a7c9c5965b055665a291a799fa95`

---

# 23. Scope and Boundaries

The current enhancement model does not establish:

- universal upgrade compatibility
- automatic migration of arbitrary production systems
- zero integration work for real applications
- universal schema evolution
- distributed upgrade coordination
- transactional migration guarantees
- production rollback guarantees
- cross-language semantic equivalence
- globally minimal program mutations
- formal machine-checked enhancement proofs
- performance or scalability superiority

The current implementation is a bounded deterministic reference model.

It uses:

- Python 3.9+
- the Python standard library
- deterministic JSON serialization
- SHA-256 identities and certificates

Production use requires independent validation and domain-specific engineering.

---

# 24. Relationship to STOCRS-R Architecture

The enhancement model is one part of the broader STOCRS-R architecture.

The architecture establishes the separation between:

- program definition
- declared inputs
- evidence
- node availability
- resolution state
- verification identities

The enhancement model focuses specifically on:

`what happens when the declared program itself changes`

Its role is therefore distinct from the:

- Proof Sketch
- Architecture Notes
- Challenge
- Verification Guide

The document is useful because versioned program evolution is a primary STOCRS-R feature rather than merely an incidental demo case.

---

# 25. Unified Enhancement Principle

The STOCRS-R v1.0 enhancement model can be summarized as:

`freeze resolver semantics`

`declare program version`

`compute program identity`

`resolve semantic inputs`

`record result certificate`

then:

`change declared program`

`compute new program identity`

`resolve the new version with the same resolver`

`record the new result certificate`

The central distinction is:

`program evolution is explicit`

rather than hidden inside an undifferentiated runtime change.

---

# Final Summary

STOCRS-R v1.0 demonstrates a bounded model of deterministic versioned program evolution.

The reference implementation shows that:

- a base program can be resolved deterministically
- the same program can be reused with different declared inputs without changing program identity
- a declared structural extension can produce a new program identity
- a declared rule-parameter change can produce another program identity
- the same frozen resolver and rulebook can resolve all demonstrated program versions
- every version remains subject to the same incompleteness, conflict, visibility, and certificate rules

The core enhancement relation is:

`declared program mutation -> changed canonical program payload -> new program identity -> deterministic new supported output`

For exact replay within one frozen program version:

`same semantic resolution inputs + complete presentation of the same available-node set -> same state + same certificate`

The enhancement model does not claim that all software upgrades can occur without operational migration work.

Its narrower contribution is explicit and testable:

**within the STOCRS-R v1.0 reference model, declared program evolution is separated from resolver evolution, input changes, and evidence changes, allowing multiple versioned program definitions to be resolved deterministically by the same frozen resolver.**

This is the STOCRS-R Enhancement Model.
