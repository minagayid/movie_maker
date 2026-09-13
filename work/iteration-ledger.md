# Iteration ledger

## Contract

- Invariant: a rights-cleared source produces a deterministic, internally consistent production package.
- Negative control: unknown or blocked source material must fail before planning.
- Independent oracle: `validate_package_dict` checks cross-manifest references separately from the generator.
- Acceptance: unit tests, CLI smoke generation, CLI validation, and clean Git state.
- Maximum repair iterations: 3 verification cycles for this MVP.

## Status

- [x] Initial architecture and vertical-slice scaffold created.
- [x] Run tests and CLI smoke flow.
- [x] Repair any verified defects.
- [ ] Create private GitHub repository and re-open remote state.

## Verification notes

- Cycle 1: 4 tests passed; found that department coverage was checked as a union.
- Cycle 2: 5 tests passed after per-manifest coverage, positive durations, and edit coverage were added.
- Cycle 3: package install succeeded after the environment's missing build dependency was installed; module-based CLI validation and blocked-source behavior are the portable checks.
