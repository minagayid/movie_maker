# movie_maker

`movie_maker` is a rights-aware production-orchestration scaffold for turning a novel, book, or story into an auditable movie package.

It models the real production chain—producer, story editor, screenplay writer, director, script supervisor, casting/voice, cinematography, production design, motion graphics, sound/music, editorial, color, and quality assurance—then connects those departments through explicit scene and asset manifests.

## What works now

The local vertical slice accepts a text story and produces:

- a project bible with source provenance and rights gating;
- a scene-by-scene adaptation plan sized to a target runtime;
- screenplay beats, dialogue placeholders, voice-over cues, visual direction, and continuity notes;
- department work orders with input/output references;
- voice-over, motion-graphics, audio, shot, and edit manifests;
- JSON suitable for downstream providers and a readable production plan;
- deterministic tests and referential-integrity validation.

The default `TemplateGenerator` is intentionally deterministic and dependency-free. It proves the orchestration contract without pretending that a template is a finished screenplay, generated voice track, rendered shot, or final feature film. Provider adapters can replace it later for an LLM, TTS, image/video model, DAW, or NLE.

## Quick start

Requires Python 3.10+.

```text
python -m pip install -e .
python -m movie_maker generate --input examples/the_lantern.txt --title "The Lantern" --author "Movie Maker Demo" --rights-status user_owned --rights-notes "Repository-owned demonstration text" --runtime 12 --output generated/the_lantern
python -m movie_maker validate --project generated/the_lantern/project.json
python -m unittest discover -s tests -v
```

The generated directory contains `project.json`, `production_plan.md`, and one JSON file per downstream manifest.

The installed `movie-maker` command is also available when Python's scripts directory is on `PATH`.

Without installation, use `python -m movie_maker` after setting `PYTHONPATH=src`.

## Architecture

```text
source text + rights metadata
            |
            v
       intake gate
            |
            v
  story planner / generator
            |
            v
     production package
       /      |       \
  departments  scenes  manifests
                         |
              voice / graphics / audio / shots / edit
```

Core modules:

- `movie_maker.models` — typed production data model;
- `movie_maker.rights` — fail-closed source-material gate;
- `movie_maker.planner` — deterministic scene and screenplay-beat planner;
- `movie_maker.departments` — production roles and work orders;
- `movie_maker.manifests` — provider-neutral downstream contracts;
- `movie_maker.pipeline` — end-to-end orchestration;
- `movie_maker.reporting` — human-readable production plan;
- `movie_maker.validation` — independent package integrity checks;
- `movie_maker.cli` — local generation and validation entry points.

## Production roles

The scaffold treats these as first-class handoffs rather than a single “AI agent”:

| Department | Role | Primary output |
| --- | --- | --- |
| Producing | Producer | schedule, budget assumptions, approvals |
| Story | Story editor | adaptation decisions and source traceability |
| Writing | Screenplay writer | scene beats, dialogue, voice-over |
| Direction | Director | intent, blocking, performance notes |
| Script | Script supervisor | continuity and version control |
| Casting | Casting director | cast brief and audition requirements |
| Voice | Voice-over director | voice performance cues and takes |
| Camera | Cinematographer | shot design and coverage |
| Design | Production designer | world, props, locations, wardrobe |
| Motion | Motion graphics designer | titles, overlays, transitions |
| Sound | Sound designer / composer | dialogue, ambience, music, mix |
| Editorial | Editor | timeline and cut decisions |
| Finishing | Colorist | look and delivery grade |
| QA | Delivery/QC lead | continuity, rights, technical checks |

## Viability and boundaries

This repository is viable today as a production-planning and orchestration foundation. It is not yet a one-command feature-film generator: high-quality adaptation, casting likeness, voice licensing, image/video consistency, music clearance, rendering capacity, editorial judgment, and human approvals still require provider integrations and review.

The rights gate accepts only `public_domain`, `licensed`, or `user_owned` source material. `unknown` and `blocked` material fails before generation. This is an engineering guardrail, not legal advice; users remain responsible for confirming rights, model terms, performer consent, likeness permissions, and music/assets clearance.

See [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md), [docs/VIABILITY.md](docs/VIABILITY.md), and [docs/ROADMAP.md](docs/ROADMAP.md) for the plan and next milestones.
