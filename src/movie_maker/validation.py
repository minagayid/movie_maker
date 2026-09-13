"""Independent checks for package completeness and cross-manifest references."""

from typing import Any


def validate_package_dict(package: dict[str, Any]) -> list[str]:
    errors: list[str] = []
    project = package.get("project")
    scenes = package.get("scenes")
    manifests = package.get("manifests")
    roles = package.get("roles")
    work_orders = package.get("work_orders")
    if not isinstance(project, dict):
        errors.append("project must be an object")
    if not isinstance(scenes, list) or not scenes:
        errors.append("scenes must be a non-empty list")
    if not isinstance(manifests, dict):
        errors.append("manifests must be an object")
    if not isinstance(roles, list) or not roles:
        errors.append("roles must be a non-empty list")
    if not isinstance(work_orders, list) or not work_orders:
        errors.append("work_orders must be a non-empty list")
    if errors:
        return errors

    scene_ids = {scene.get("scene_id") for scene in scenes if isinstance(scene, dict)}
    if None in scene_ids:
        errors.append("every scene requires scene_id")
    if len(scene_ids) != len(scenes):
        errors.append("scene_id values must be unique")

    for name in ("voice_over", "motion_graphics", "audio"):
        items = manifests.get(name, {}).get("items", [])
        seen_scene_ids: list[str] = []
        for item in items:
            seen_scene_ids.append(item.get("scene_id"))
            if item.get("scene_id") not in scene_ids:
                errors.append(f"{name} references unknown scene {item.get('scene_id')!r}")
        if set(seen_scene_ids) != scene_ids or len(seen_scene_ids) != len(scene_ids):
            errors.append(f"{name} must contain exactly one item for every scene")

    shot_items = manifests.get("shots", {}).get("items", [])
    shot_ids = {item.get("shot_id") for item in shot_items}
    if None in shot_ids or len(shot_ids) != len(shot_items):
        errors.append("shot_id values must be present and unique")
    for item in shot_items:
        if item.get("scene_id") not in scene_ids:
            errors.append(f"shots references unknown scene {item.get('scene_id')!r}")
        if not isinstance(item.get("duration_seconds"), int) or item.get("duration_seconds") <= 0:
            errors.append(f"shot {item.get('shot_id')!r} must have a positive integer duration")

    edit_scene_ids = []
    for entry in manifests.get("edit", {}).get("sequence", []):
        edit_scene_ids.append(entry.get("scene_id"))
        if entry.get("scene_id") not in scene_ids:
            errors.append(f"edit references unknown scene {entry.get('scene_id')!r}")
        for shot_id in entry.get("shot_ids", []):
            if shot_id not in shot_ids:
                errors.append(f"edit references unknown shot {shot_id!r}")
    if set(edit_scene_ids) != scene_ids or len(edit_scene_ids) != len(scene_ids):
        errors.append("edit sequence must contain exactly one entry for every scene")

    role_names = {role.get("role") for role in roles}
    order_roles = {order.get("role") for order in work_orders}
    if role_names != order_roles:
        errors.append("every production role must have exactly one work order")
    return errors
