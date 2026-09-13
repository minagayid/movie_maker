"""Domain models shared by the planner, departments, manifests, and CLI."""

from dataclasses import asdict, dataclass, field
from typing import Any


@dataclass(frozen=True)
class SourceMaterial:
    title: str
    author: str
    text: str
    rights_status: str
    rights_notes: str = ""


@dataclass(frozen=True)
class ProjectSpec:
    title: str
    source: SourceMaterial
    target_runtime_minutes: int = 90
    target_rating: str = "PG-13"
    visual_style: str = "cinematic naturalism"
    language: str = "en"
    project_id: str = ""


@dataclass
class Scene:
    scene_id: str
    sequence: int
    heading: str
    source_excerpt: str
    synopsis: str
    emotional_beat: str
    duration_seconds: int
    characters: list[str] = field(default_factory=list)
    dialogue: list[dict[str, str]] = field(default_factory=list)
    voiceover: str = ""
    visual_prompt: str = ""
    motion_graphics: list[str] = field(default_factory=list)
    continuity_notes: list[str] = field(default_factory=list)


@dataclass(frozen=True)
class ProductionRole:
    department: str
    role: str
    purpose: str
    deliverables: tuple[str, ...]


@dataclass(frozen=True)
class WorkOrder:
    department: str
    role: str
    tasks: tuple[str, ...]
    input_refs: tuple[str, ...]
    output_refs: tuple[str, ...]


@dataclass
class ProductionPackage:
    project: ProjectSpec
    scenes: list[Scene]
    roles: list[ProductionRole]
    work_orders: list[WorkOrder]
    manifests: dict[str, Any]
    warnings: list[str] = field(default_factory=list)

    def to_dict(self) -> dict[str, Any]:
        """Return a JSON-serializable representation of the package."""

        return asdict(self)
