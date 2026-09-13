"""Deterministic story-to-scene planning with a provider replacement seam."""

from __future__ import annotations

import re
from dataclasses import dataclass
from hashlib import sha256
from typing import Protocol

from .models import ProjectSpec, Scene


@dataclass(frozen=True)
class SceneContent:
    """Provider-neutral content returned for one planned scene."""

    heading: str
    synopsis: str
    emotional_beat: str
    characters: tuple[str, ...]
    dialogue: tuple[dict[str, str], ...]
    voiceover: str
    visual_prompt: str
    motion_graphics: tuple[str, ...]
    continuity_notes: tuple[str, ...]


class ContentGenerator(Protocol):
    """Provider seam for model-backed screenplay and scene generation."""

    def generate(self, spec: ProjectSpec, excerpt: str, sequence: int, total: int) -> SceneContent:
        ...


class TemplateGenerator:
    """A deterministic local generator used for tests and offline demos.

    This is a structural baseline, not a claim of literary or cinematic quality.
    A model-backed adapter can implement the same ``generate`` method.
    """

    _beats = (
        "setup",
        "inciting incident",
        "first threshold",
        "rising complication",
        "midpoint reversal",
        "pressure mounts",
        "all-is-lost turn",
        "final choice",
        "resolution",
    )

    def generate(self, spec: ProjectSpec, excerpt: str, sequence: int, total: int) -> SceneContent:
        progress = (sequence - 1) / max(total - 1, 1)
        beat = self._beats[min(len(self._beats) - 1, round(progress * (len(self._beats) - 1)))]
        clean = re.sub(r"\s+", " ", excerpt).strip()
        words = clean.split()
        title_seed = " ".join(words[:5]) if words else "Untitled beat"
        title = f"{beat.title()}: {title_seed.title()}"
        style = spec.visual_style
        synopsis = f"Adapt the source beat into a {beat} sequence while preserving its core intent: {clean}"
        dialogue = ({"speaker": "PROTAGONIST", "line": "The choice is ours now."},)
        voiceover = f"VO placeholder: {clean}"
        visual_prompt = f"{style}; story-driven composition; {beat}; source beat: {clean}"
        motion_graphics = (f"Lower third for scene {sequence:03d}", "Chapter transition if editorially approved")
        continuity = ("Track protagonist objective and emotional state into the next scene",)
        characters = ("Protagonist", "Supporting cast — to be cast")
        return SceneContent(
            heading=f"INT./EXT. — {title.upper()} — TIME TBD",
            synopsis=synopsis,
            emotional_beat=beat,
            characters=characters,
            dialogue=dialogue,
            voiceover=voiceover,
            visual_prompt=visual_prompt,
            motion_graphics=motion_graphics,
            continuity_notes=continuity,
        )


def project_id_for(spec: ProjectSpec) -> str:
    """Create a stable ID without storing the source text in the identifier."""

    slug = re.sub(r"[^a-z0-9]+", "-", spec.title.lower()).strip("-") or "untitled"
    digest = sha256(spec.source.text.encode("utf-8")).hexdigest()[:10]
    return f"{slug}-{digest}"


def _source_segments(text: str) -> list[str]:
    paragraphs = [re.sub(r"\s+", " ", p).strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if paragraphs:
        return paragraphs
    sentences = [s.strip() for s in re.split(r"(?<=[.!?])\s+", text) if s.strip()]
    return sentences or [text.strip()]


def _scene_count(runtime_minutes: int) -> int:
    # Five minutes per scene is a planning baseline; providers may later split scenes.
    return max(3, min(120, round(runtime_minutes / 5)))


def _scene_durations(runtime_minutes: int, count: int) -> list[int]:
    total_seconds = runtime_minutes * 60
    base, remainder = divmod(total_seconds, count)
    return [base + (1 if index < remainder else 0) for index in range(count)]


def build_scenes(spec: ProjectSpec, generator: ContentGenerator | None = None) -> list[Scene]:
    generator = generator or TemplateGenerator()
    segments = _source_segments(spec.source.text)
    count = _scene_count(spec.target_runtime_minutes)
    durations = _scene_durations(spec.target_runtime_minutes, count)
    scenes: list[Scene] = []
    for index, duration in enumerate(durations, start=1):
        excerpt = segments[(index - 1) % len(segments)]
        content = generator.generate(spec, excerpt, index, count)
        scenes.append(
            Scene(
                scene_id=f"sc-{index:03d}",
                sequence=index,
                heading=content.heading,
                source_excerpt=excerpt,
                synopsis=content.synopsis,
                emotional_beat=content.emotional_beat,
                duration_seconds=duration,
                characters=list(content.characters),
                dialogue=[dict(line) for line in content.dialogue],
                voiceover=content.voiceover,
                visual_prompt=content.visual_prompt,
                motion_graphics=list(content.motion_graphics),
                continuity_notes=list(content.continuity_notes),
            )
        )
    return scenes
