"""Independent checks for package completeness and cross-manifest references."""

from typing import Any


def _manifest_rows(
    manifests: dict[str, Any],
    name: str,
    key: str,
    errors: list[str],
) -> list[Any]:
    manifest = manifests.get(name)
    if not isinstance(manifest, dict):
        errors.append(f"{name} must be an object")
        return []
    rows = manifest.get(key)
    if not isinstance(rows, list):
        errors.append(f"{name}.{key} must be an array")
        return []
    return rows


def _valid_ids(rows: list[Any], field: str, label: str, errors: list[str]) -> list[str]:
    values: list[str] = []
    for index, row in enumerate(rows):
        if not isinstance(row, dict):
            errors.append(f"{label} item {index} must be an object")
            continue
        value = row.get(field)
        if not isinstance(value, str) or not value.strip():
            errors.append(f"every {label} item requires {field}")
            continue
        values.append(value)
    if len(values) != len(set(values)):
        errors.append(f"{field} values must be unique")
    return values


def validate_package_dict(package: Any) -> list[str]:
    """Return structural errors without raising for malformed external JSON."""
    if not isinstance(package, dict):
        return ["package must be an object"]

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
        scenes = []
    if not isinstance(manifests, dict):
        errors.append("manifests must be an object")
        manifests = {}
    if not isinstance(roles, list) or not roles:
        errors.append("roles must be a non-empty list")
        roles = []
    if not isinstance(work_orders, list) or not work_orders:
        errors.append("work_orders must be a non-empty list")
        work_orders = []

    scene_ids = _valid_ids(scenes, "scene_id", "scene", errors)
    scene_id_set = set(scene_ids)

    for name in ("voice_over", "motion_graphics", "audio"):
        rows = _manifest_rows(manifests, name, "items", errors)
        row_scene_ids = []
        for index, row in enumerate(rows):
            if not isinstance(row, dict):
                errors.append(f"{name} item {index} must be an object")
                continue
            scene_id = row.get("scene_id")
            if isinstance(scene_id, str):
                row_scene_ids.append(scene_id)
            if not isinstance(scene_id, str) or scene_id not in scene_id_set:
                errors.append(f"{name} references unknown scene {scene_id!r}")
        if set(row_scene_ids) != scene_id_set or len(row_scene_ids) != len(scene_id_set):
            errors.append(f"{name} must contain exactly one item for every scene")

    shot_rows = _manifest_rows(manifests, "shots", "items", errors)
    shot_ids = _valid_ids(shot_rows, "shot_id", "shot", errors)
    shot_id_set = set(shot_ids)
    for index, row in enumerate(shot_rows):
        if not isinstance(row, dict):
            continue
        scene_id = row.get("scene_id")
        if not isinstance(scene_id, str) or scene_id not in scene_id_set:
            errors.append(f"shots references unknown scene {scene_id!r}")
        duration = row.get("duration_seconds")
        if isinstance(duration, bool) or not isinstance(duration, int) or duration <= 0:
            errors.append(f"shot {row.get('shot_id')!r} must have a positive integer duration")

    edit_rows = _manifest_rows(manifests, "edit", "sequence", errors)
    edit_scene_ids = []
    for index, row in enumerate(edit_rows):
        if not isinstance(row, dict):
            errors.append(f"edit item {index} must be an object")
            continue
        scene_id = row.get("scene_id")
        if isinstance(scene_id, str):
            edit_scene_ids.append(scene_id)
        if not isinstance(scene_id, str) or scene_id not in scene_id_set:
            errors.append(f"edit references unknown scene {scene_id!r}")
        referenced_shots = row.get("shot_ids")
        if not isinstance(referenced_shots, list):
            errors.append(f"edit entry for scene {scene_id!r} must have a shot_ids array")
            continue
        for shot_id in referenced_shots:
            if not isinstance(shot_id, str) or shot_id not in shot_id_set:
                errors.append(f"edit references unknown shot {shot_id!r}")
    if set(edit_scene_ids) != scene_id_set or len(edit_scene_ids) != len(scene_id_set):
        errors.append("edit sequence must contain exactly one entry for every scene")

    def role_ids(rows: list[Any], label: str) -> list[str]:
        values: list[str] = []
        for index, row in enumerate(rows):
            if not isinstance(row, dict):
                errors.append(f"{label} item {index} must be an object")
                continue
            role = row.get("role")
            if not isinstance(role, str) or not role.strip():
                errors.append(f"every {label} item requires role")
                continue
            values.append(role)
        if len(values) != len(set(values)):
            errors.append(f"{label} role values must be unique")
        return values

    role_names = role_ids(roles, "production role")
    order_roles = role_ids(work_orders, "work order")
    if set(role_names) != set(order_roles) or len(role_names) != len(order_roles):
        errors.append("every production role must have exactly one work order")
    return errors
