# Architecture

## Design objective

The system coordinates creative departments and media-producing services without coupling the project to one model vendor. Every stage receives structured inputs and emits named artifacts, so a human or another provider can replace an individual stage without rewriting the pipeline.

## Current data flow

1. `SourceMaterial` stores the text, attribution, rights status, and audit notes.
2. `rights.assert_source_is_producible` fails closed for unknown or blocked material.
3. `planner.build_scenes` creates a stable scene list whose durations sum exactly to the requested runtime.
4. `departments.build_work_orders` creates one accountable handoff for each production role.
5. `manifests.build_manifests` creates provider-neutral contracts for voice, graphics, audio, shots, and editing.
6. `validation.validate_package_dict` checks scene IDs, shot IDs, coverage, and role/work-order parity independently of the generator.
7. `reporting.production_plan_markdown` creates a reviewable human document.

## Extension seams

The first provider seam is `TemplateGenerator.generate`. A production adapter should return the same `SceneContent` shape and record provider name, model version, prompt/input hash, cost, and review status in the package metadata.

Future adapters should be isolated behind interfaces for:

- language-model adaptation and screenplay drafting;
- casting and consent tracking;
- text-to-speech with voice identity/consent metadata;
- image/video generation with seed, model, and asset provenance;
- motion-graphics templates;
- music/SFX and DAW export;
- NLE timeline import/export;
- render farm, storage, and delivery QC.

## Non-negotiable invariants

- Uncleared source material never enters generation.
- Every scene has a stable ID and a runtime allocation.
- Every scene is covered by voice, graphics, audio, and edit references.
- Every shot belongs to a known scene and every edit reference points to a known shot.
- Human review remains visible as a status in downstream work orders.
