"""Human-readable rendering of a production package."""

from .models import ProductionPackage


def production_plan_markdown(package: ProductionPackage) -> str:
    project = package.project
    lines = [
        f"# Production Plan — {project.title}",
        "",
        f"- Project ID: `{project.project_id}`",
        f"- Source: {project.source.title} — {project.source.author}",
        f"- Rights status: `{project.source.rights_status}`",
        f"- Target runtime: {project.target_runtime_minutes} minutes",
        f"- Rating target: {project.target_rating}",
        f"- Visual style: {project.visual_style}",
        "",
        "## Warnings",
        "",
    ]
    lines.extend(f"- {warning}" for warning in package.warnings)
    lines.extend(["", "## Department handoffs", ""])
    for order in package.work_orders:
        lines.extend([f"### {order.role} ({order.department})", ""])
        lines.extend(f"- {task}" for task in order.tasks)
        lines.append(f"- Outputs: {', '.join(order.output_refs)}")
        lines.append("")
    lines.extend(["## Scene plan", ""])
    for scene in package.scenes:
        lines.extend(
            [
                f"### {scene.sequence:03d}. {scene.heading}",
                "",
                f"- Duration: {scene.duration_seconds}s",
                f"- Emotional beat: {scene.emotional_beat}",
                f"- Source excerpt: {scene.source_excerpt}",
                f"- Synopsis: {scene.synopsis}",
                f"- Characters: {', '.join(scene.characters)}",
                f"- Voice-over: {scene.voiceover}",
                f"- Motion graphics: {', '.join(scene.motion_graphics)}",
                "",
            ]
        )
    lines.extend(["## Manifest files", "", "- `project.json`", "- `voice_over.json`", "- `motion_graphics.json`", "- `audio.json`", "- `shots.json`", "- `edit.json`", ""])
    return "\n".join(lines)
