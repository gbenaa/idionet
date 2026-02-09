# Product 0005 — Admission and Registration Primitive

**Version:** 0.1  
**Status:** Candidate productive primitive  
**Authority:** Sandboxed Production Ecology  
**Governing specification:** Product 0001 v0.1  
**Revision mode:** Revision-only (no replacement)

---

## Purpose

This product defines a stabilised way of producing products within the Sandboxed Production Ecology.

It captures the minimal pattern by which a product becomes authoritative: admission followed by registration.

---

## Definition

A product is considered validly produced within the ecology when the following steps occur in order:

1. The artefact is explicitly admitted as a product.
2. The admission is recorded in the Product Register.

Both steps are required.

---

## Inputs

- A candidate artefact intended to function as a product.

---

## Process

1. Create the artefact in the governed container.
2. Commit the artefact as an admitted product.
3. Revise the Product Register to record the admission.
4. Commit the revised register.

---

## Outputs

- An admitted product.
- A corresponding register entry.

---

## Provenance

This pattern is derived from the repeated admission of Products 0001 through 0004.

---

## Validation Status

This productive primitive is considered a candidate.

It becomes validated only if:
- it continues to be used without exception,
- no alternative admission path emerges,
- and no product is found to exist without both steps.

---

## Failure Modes

This primitive fails if:
- a product is treated as authoritative without being registered,
- the register is bypassed or weakened,
- or admission becomes implicit rather than explicit.

---

## Self-Application

This productive primitive is itself a product and must be admitted and registered to have standing.

---

## NOTE (intentional invalid change)

This sentence was added without a version increment to test version discipline.

---

**End of Product 0005 (v0.1)**
