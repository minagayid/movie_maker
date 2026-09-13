"""Production department definitions and explicit handoff work orders."""

from .models import ProductionRole, ProjectSpec, Scene, WorkOrder


def default_roles() -> list[ProductionRole]:
    return [
        ProductionRole("Producing", "Producer", "Own scope, approvals, schedule, and budget assumptions", ("schedule.json", "approval_gates.json")),
        ProductionRole("Story", "Story editor", "Protect source intent and document adaptation decisions", ("adaptation_notes.md",)),
        ProductionRole("Writing", "Screenplay writer", "Turn source beats into screenplay-ready scenes", ("screenplay.json",)),
        ProductionRole("Direction", "Director", "Define performance, blocking, tone, and editorial intent", ("director_notes.json",)),
        ProductionRole("Script", "Script supervisor", "Maintain continuity, versions, and scene-state tracking", ("continuity_log.json",)),
        ProductionRole("Casting", "Casting director", "Define cast requirements and audition briefs", ("casting_brief.json",)),
        ProductionRole("Voice", "Voice-over director", "Direct narration, dialogue performance, and take selection", ("voice_manifest.json",)),
        ProductionRole("Camera", "Cinematographer", "Design coverage, lenses, movement, and shot priorities", ("shot_manifest.json",)),
        ProductionRole("Design", "Production designer", "Define locations, props, wardrobe, and visual world", ("design_bible.json",)),
        ProductionRole("Motion", "Motion graphics designer", "Create titles, overlays, maps, and transitions", ("motion_manifest.json",)),
        ProductionRole("Sound", "Sound designer / composer", "Plan dialogue, ambience, effects, score, and mix", ("audio_manifest.json",)),
        ProductionRole("Editorial", "Editor", "Assemble the timeline and track cut decisions", ("edit_manifest.json",)),
        ProductionRole("Finishing", "Colorist", "Apply a consistent look and delivery grade", ("color_notes.json",)),
        ProductionRole("QA", "Delivery/QC lead", "Check rights, continuity, technical output, and approvals", ("qc_report.json",)),
    ]


def build_work_orders(project: ProjectSpec, scenes: list[Scene], roles: list[ProductionRole]) -> list[WorkOrder]:
    scene_refs = tuple(scene.scene_id for scene in scenes)
    orders: list[WorkOrder] = []
    for role in roles:
        tasks = (
            f"Review project {project.project_id or project.title!r}",
            f"Process scenes: {', '.join(scene_refs)}",
            f"Record review status and unresolved questions for the {role.department} handoff",
        )
        orders.append(
            WorkOrder(
                department=role.department,
                role=role.role,
                tasks=tasks,
                input_refs=("project.json", "production_plan.md"),
                output_refs=role.deliverables,
            )
        )
    return orders
