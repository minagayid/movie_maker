# Viability review

## Verdict

The repository is viable as a deterministic pre-production/orchestration MVP. It is not yet viable as an autonomous full-length movie factory because the expensive and quality-critical media stages are represented as contracts, not implemented providers.

## Evidence in this scaffold

| Area | Evidence | Confidence |
| --- | --- | --- |
| Story intake | UTF-8 text plus attribution and rights metadata | High |
| Rights boundary | Unknown/blocked sources fail before planning | High |
| Runtime planning | Scene durations sum exactly to the target runtime | High |
| Department structure | 14 accountable roles and matching work orders | High |
| Asset handoffs | Voice, graphics, audio, shots, and edit manifests | High |
| Referential integrity | Independent validator and regression tests | High |
| Literary quality | Template baseline only | Low |
| Generated media quality | Not implemented | None yet |
| Feature-film economics | Provider costs and render capacity not measured | None yet |

## What would make it production-ready

1. Add provider adapters with recorded provenance, retries, rate limits, and cost budgets.
2. Add a screenplay-quality review gate for plot coverage, character continuity, pacing, dialogue, and source traceability.
3. Add asset-level consent and licensing records for voices, faces, music, locations, and training/output terms.
4. Add temporal consistency checks for generated shots and audio synchronization.
5. Add a render/export adapter and test against a real NLE interchange format.
6. Run a pilot on one short, rights-cleared story and measure human revision time, asset rejection rate, runtime drift, and total cost.

## Claim boundary

“Generate a production package” is supported now. “Generate a finished full-length movie” is a roadmap goal, not a current capability claim.
