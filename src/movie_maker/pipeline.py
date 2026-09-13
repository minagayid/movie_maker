"""End-to-end orchestration from source material to a production package."""

from __future__ import annotations

from dataclasses import replace

from .departments import build_work_orders, default_roles
from .manifests import build_manifests
from .models import ProjectSpec, ProductionPackage
from .planner import ContentGenerator, TemplateGenerator, build_scenes, project_id_for
from .rights import assert_source_is_producible


class MovieMaker:
    """Build a production package with a replaceable content generator."""

    def __init__(self, generator: ContentGenerator | None = None) -> None:
        self.generator = generator or TemplateGenerator()

    def generate(self, spec: ProjectSpec) -> ProductionPackage:
        if spec.target_runtime_minutes < 1 or spec.target_runtime_minutes > 600:
            raise ValueError("target_runtime_minutes must be between 1 and 600")
        assert_source_is_producible(spec.source)
        project = spec if spec.project_id else replace(spec, project_id=project_id_for(spec))
        scenes = build_scenes(project, self.generator)
        roles = default_roles()
        work_orders = build_work_orders(project, scenes, roles)
        manifests = build_manifests(project, scenes)
        warnings = [
            "TemplateGenerator output is a planning baseline and requires human creative review.",
            "Media assets, performer consent, provider terms, music clearance, and final renders are not produced by this local package.",
        ]
        return ProductionPackage(project, scenes, roles, work_orders, manifests, warnings)
