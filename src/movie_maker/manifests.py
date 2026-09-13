"""Provider-neutral downstream manifests for a future media pipeline."""

from typing import Any

from .models import ProjectSpec, Scene


def build_manifests(project: ProjectSpec, scenes: list[Scene]) -> dict[str, Any]:
    voice_over = []
    motion_graphics = []
    audio = []
    shots = []
    sequence = []

    for scene in scenes:
        voice_over.append(
            {
                "asset_id": f"vo-{scene.scene_id}",
                "scene_id": scene.scene_id,
                "text": scene.voiceover,
                "speaker": "narrator",
                "status": "planned",
                "provider": None,
                "consent_ref": None,
            }
        )
        motion_graphics.append(
            {
                "asset_id": f"gfx-{scene.scene_id}",
                "scene_id": scene.scene_id,
                "brief": scene.motion_graphics,
                "aspect_ratio": "16:9",
                "status": "planned",
            }
        )
        audio.append(
            {
                "asset_id": f"aud-{scene.scene_id}",
                "scene_id": scene.scene_id,
                "layers": ["dialogue", "ambience", "effects", "music"],
                "mix_target_lufs": -14,
                "status": "planned",
            }
        )
        first_duration = max(1, scene.duration_seconds // 2)
        shot_specs = (
            ("establishing", first_duration),
            ("coverage", scene.duration_seconds - first_duration),
        )
        shot_ids = []
        for shot_number, (shot_type, duration) in enumerate(shot_specs, start=1):
            shot_id = f"sh-{scene.scene_id}-{shot_number:02d}"
            shot_ids.append(shot_id)
            shots.append(
                {
                    "shot_id": shot_id,
                    "scene_id": scene.scene_id,
                    "shot_type": shot_type,
                    "duration_seconds": duration,
                    "visual_prompt": scene.visual_prompt,
                    "status": "planned",
                }
            )
        sequence.append({"scene_id": scene.scene_id, "shot_ids": shot_ids})

    return {
        "voice_over": {"schema_version": "0.1", "items": voice_over},
        "motion_graphics": {"schema_version": "0.1", "items": motion_graphics},
        "audio": {"schema_version": "0.1", "items": audio},
        "shots": {"schema_version": "0.1", "items": shots},
        "edit": {
            "schema_version": "0.1",
            "timeline_id": f"timeline-{project.project_id}",
            "frame_rate": 24,
            "resolution": "3840x2160",
            "sequence": sequence,
            "status": "planned",
        },
    }
