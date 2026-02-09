# Product 0012 — Invalid Reference Violation Record (Product 0011 -> PRODUCT-0010)

**Version:** 0.1  
**Status:** Admitted  
**Authority:** Sandboxed Production Ecology  
**Governing specification:** Product 0001 v0.1  
**Related primitive:** Product 0005 v0.2  
**Revision mode:** Revision-only (no replacement)

---

## Purpose

To record a violation in which an admitted product referenced an artefact that was not registered, attempting to confer standing by reference.

---

## Violation

- **Product affected:** PRODUCT-0011
- **Violating commit:** 052e411dab5000b1879c411272eb2ec264e7845d
- **Unregistered artefact referenced:** PRODUCT-0010_Unregistered-Reference-Target.md
- **Violation type:** Reference to unregistered artefact within an admitted product

---

## Rule

An admitted product may not treat an artefact as authoritative, operative, or standing-bearing unless that artefact is recorded in the Product Register.

---

## Disposition

- The reference in Product 0011 is declared invalid.
- The artefact PRODUCT-0010 remains without standing until explicitly registered.
- Correction occurs only by:
  - registering PRODUCT-0010, and then revising Product 0011 to reference it validly, or
  - revising Product 0011 to remove the reference.

---

**End of Product 0012 (v0.1)**
